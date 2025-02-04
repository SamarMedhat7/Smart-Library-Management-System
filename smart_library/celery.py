import os
from celery import Celery 

os.environ.setdefault('DJANGO_SETTINGS_MODULE','smart_library.settings')
app = Celery('smart_library')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
