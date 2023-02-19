# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import os
from django.apps import apps
# set the default Django settings module for the 'celery' program.
from django.utils import timezone
from kombu import Queue, Exchange
from celery import Celery, platforms, Task

platforms.C_FORCE_ROOT = True
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ipam_boost.settings')

app = Celery('ipam_boost')
app.now = timezone.now
app.config_from_object('django.conf:settings', namespace='CELERY')

# default_exchange = Exchange('default', type='direct')
django_open_ipam_exchange = Exchange('django_open_ipam', type='direct')

app.conf.task_time_limit = 86400
app.conf.worker_prefetch_multiplier = 10
app.conf.worker_max_tasks_per_child = 100
app.conf.task_default_queue = 'django_open_ipam'
app.conf.task_default_exchange = 'django_open_ipam'
app.conf.task_default_routing_key = 'django_open_ipam'
app.conf.task_default_exchange_type = 'direct'
app.conf.task_queues = (
    # Queue('default', default_exchange, routing_key='default'),
    Queue('django_open_ipam', django_open_ipam_exchange, routing_key='django_open_ipam'),
)

app.autodiscover_tasks(lambda: [n.name for n in apps.get_app_configs()])


class IpAmTask(Task):

    def run(self, *args, **kwargs):
        pass

    max_retries = 1
    autoretry_for = (Exception, KeyError, RuntimeError)
    retry_kwargs = {'max_retries': 1}
    retry_backoff = False

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        print(str(einfo))
        return super(IpAmTask, self).on_failure(exc, task_id, args, kwargs, einfo)

    def on_retry(self, exc, task_id, args, kwargs, einfo):
        # print('task retry, reason: {0}'.format(exc))
        print(str(einfo))
        return super(IpAmTask, self).on_failure(exc, task_id, args, kwargs, einfo)