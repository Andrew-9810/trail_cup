import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trail_cup.settings')

app = Celery('trail_cup')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()