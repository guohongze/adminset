from __future__ import absolute_import, unicode_literals

import celery
import pytest

from celery import uuid
from celery import states

from django_celery_results.backends.database import DatabaseBackend


class SomeClass(object):

    def __init__(self, data):
        self.data = data


@pytest.mark.django_db()
@pytest.mark.usefixtures('depends_on_current_app')
class test_DatabaseBackend:

    @pytest.fixture(autouse=True)
    def setup_backend(self):
        self.app.conf.result_serializer = 'json'
        self.app.conf.result_backend = (
            'django_celery_results.backends:DatabaseBackend')
        self.b = DatabaseBackend(app=self.app)

    def test_backend__pickle_serialization(self):
        self.app.conf.result_serializer = 'pickle'
        self.app.conf.accept_content = {'pickle', 'json'}
        self.b = DatabaseBackend(app=self.app)

        tid2 = uuid()
        result = {'foo': 'baz', 'bar': SomeClass(12345)}
        self.b.mark_as_done(tid2, result)
        # is serialized properly.
        rindb = self.b.get_result(tid2)
        assert rindb.get('foo') == 'baz'
        assert rindb.get('bar').data == 12345

        tid3 = uuid()
        try:
            raise KeyError('foo')
        except KeyError as exception:
            self.b.mark_as_failure(tid3, exception)

        assert self.b.get_status(tid3) == states.FAILURE
        assert isinstance(self.b.get_result(tid3), KeyError)

    def xxx_backend(self):
        tid = uuid()

        assert self.b.get_status(tid) == states.PENDING
        assert self.b.get_result(tid) is None

        self.b.mark_as_done(tid, 42)
        assert self.b.get_status(tid) == states.SUCCESS
        assert self.b.get_result(tid) == 42

        tid2 = uuid()
        try:
            raise KeyError('foo')
        except KeyError as exception:
            self.b.mark_as_failure(tid2, exception)

        assert self.b.get_status(tid2) == states.FAILURE
        assert isinstance(self.b.get_result(tid2), KeyError)

    def test_forget(self):
        tid = uuid()
        self.b.mark_as_done(tid, {'foo': 'bar'})
        x = self.app.AsyncResult(tid)
        assert x.result.get('foo') == 'bar'
        x.forget()
        if celery.VERSION[0:3] == (3, 1, 10):
            # bug in 3.1.10 means result did not clear cache after forget.
            x._cache = None
        assert x.result is None
