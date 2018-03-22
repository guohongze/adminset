from __future__ import absolute_import, unicode_literals

import pytest

from datetime import datetime, timedelta

from celery import states, uuid
from celery.five import text_t

from django_celery_results.models import TaskResult
from django_celery_results.utils import now


@pytest.mark.django_db()
@pytest.mark.usefixtures('depends_on_current_app')
class test_Models:

    @pytest.fixture(autouse=True)
    def setup_app(self, app):
        self.app = app
        self.app.conf.result_serializer = 'pickle'
        self.app.conf.result_backend = (
            'django_celery_results.backends:DatabaseBackend')

    def create_task_result(self):
        id = uuid()
        taskmeta, created = TaskResult.objects.get_or_create(task_id=id)
        return taskmeta

    def test_taskmeta(self, ctype='application/json', cenc='utf-8'):
        m1 = self.create_task_result()
        m2 = self.create_task_result()
        m3 = self.create_task_result()
        assert text_t(m1).startswith('<Task:')
        assert m1.task_id
        assert isinstance(m1.date_done, datetime)

        assert TaskResult.objects.get_task(m1.task_id).task_id == m1.task_id
        assert TaskResult.objects.get_task(m1.task_id).status != states.SUCCESS
        TaskResult.objects.store_result(
            ctype, cenc, m1.task_id, True, status=states.SUCCESS)
        TaskResult.objects.store_result(
            ctype, cenc, m2.task_id, True, status=states.SUCCESS)
        assert TaskResult.objects.get_task(m1.task_id).status == states.SUCCESS
        assert TaskResult.objects.get_task(m2.task_id).status == states.SUCCESS

        # Have to avoid save() because it applies the auto_now=True.
        TaskResult.objects.filter(
            task_id=m1.task_id
        ).update(date_done=now() - timedelta(days=10))

        expired = TaskResult.objects.get_all_expired(
            self.app.conf.result_expires,
        )
        assert m1 in expired
        assert m2 not in expired
        assert m3 not in expired

        TaskResult.objects.delete_expired(
            self.app.conf.result_expires,
        )
        assert m1 not in TaskResult.objects.all()
