from celery import Celery

# from __future__ import absolute_import, unicode_literals
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Library.settings')

app = Celery('Library')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
