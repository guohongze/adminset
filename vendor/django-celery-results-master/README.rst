=====================================================================
 Celery Result Backends using the Django ORM/Cache framework.
=====================================================================

|build-status| |coverage| |license| |wheel| |pyversion| |pyimp|

:Version: 1.0.1
:Web: http://django-celery-results.readthedocs.io/
:Download: http://pypi.python.org/pypi/django-celery-results
:Source: http://github.com/celery/django-celery-results
:Keywords: django, celery, database, results

About
=====

This extension enables you to store Celery task results using the Django ORM.

It defines a single model (``django_celery_results.models.TaskResult``)
used to store task results, and you can query this database table like
any other Django model.

Installing
==========

The installation instructions for this extension is available
from the `Celery documentation`_:

http://docs.celeryproject.org/en/latest/django/first-steps-with-django.html#django-celery-results-using-the-django-orm-cache-as-a-result-backend


.. _`Celery documentation`:
    http://docs.celeryproject.org/en/latest/django/first-steps-with-django.html#django-celery-results-using-the-django-orm-cache-as-a-result-backend

.. _installation:

Installation
============

You can install django-celery-results either via the Python Package Index (PyPI)
or from source.

To install using `pip`,::

    $ pip install -U django-celery-results

.. _installing-from-source:

Downloading and installing from source
--------------------------------------

Download the latest version of django-celery-results from
http://pypi.python.org/pypi/django-celery-results

You can install it by doing the following,::

    $ tar xvfz django-celery-results-0.0.0.tar.gz
    $ cd django-celery-results-0.0.0
    $ python setup.py build
    # python setup.py install

The last command must be executed as a privileged user if
you are not currently using a virtualenv.

.. _installing-from-git:

Using the development version
-----------------------------

With pip
~~~~~~~~

You can install the latest snapshot of django-celery-results using the following
pip command::

    $ pip install https://github.com/celery/django-celery-results/zipball/master#egg=django-celery-results

.. |build-status| image:: https://secure.travis-ci.org/celery/django-celery-results.png?branch=master
    :alt: Build status
    :target: https://travis-ci.org/celery/django-celery-results

.. |coverage| image:: https://codecov.io/github/celery/django-celery-results/coverage.svg?branch=master
    :target: https://codecov.io/github/celery/django-celery-results?branch=master

.. |license| image:: https://img.shields.io/pypi/l/django-celery-results.svg
    :alt: BSD License
    :target: https://opensource.org/licenses/BSD-3-Clause

.. |wheel| image:: https://img.shields.io/pypi/wheel/django-celery-results.svg
    :alt: django-celery-results can be installed via wheel
    :target: http://pypi.python.org/pypi/django-celery-results/

.. |pyversion| image:: https://img.shields.io/pypi/pyversions/django-celery-results.svg
    :alt: Supported Python versions.
    :target: http://pypi.python.org/pypi/django-celery-results/

.. |pyimp| image:: https://img.shields.io/pypi/implementation/django-celery-results.svg
    :alt: Support Python implementations.
    :target: http://pypi.python.org/pypi/django-celery-results/

