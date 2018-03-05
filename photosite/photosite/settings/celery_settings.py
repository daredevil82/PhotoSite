# Celery configuration for various asynchronous tasks in support of this project

from __future__ import absolute_import

from kombu import Queue

CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json', ]

CELERY_DEFAULT_QUEUE = 'default',
CELERY_QUEUES = (
    Queue('default', routing_key = 'default.#')
)