from __future__ import absolute_import, unicode_literals
import os
import dotenv
from celery import Celery
from kombu import Queue

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'airflow_aas.settings')
dotenv.read_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

app = Celery('airflow_aas')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')


app.conf.task_default_queue = 'k8s_tasks'
app.conf.task_queues = (
    Queue('k8s_tasks', routing_key='k8s.#'),
)

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


# @app.task(bind=True)
# def debug_task(self):
#     print('Request: {0!r}'.format(self.request))
