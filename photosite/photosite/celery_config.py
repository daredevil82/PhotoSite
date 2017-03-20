from __future__ import absolute_import

import os

from celery import Celery
from django.conf import settings
from photosite.settings import CELERY

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'photosite.settings')

app = Celery('photosite',
             backend = CELERY['backend'],
             broker = CELERY['broker'],
             include = ['app.tasks.image'])

app.config_from_object('django.conf:settings')
app.config_from_object(settings)
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

