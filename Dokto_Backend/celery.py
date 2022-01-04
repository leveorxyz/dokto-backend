from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

# setting the Django settings module.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Dokto_Backend.settings')
app = Celery('Dokto_Backend')
app.config_from_object('django.conf:settings', namespace='CELERY')


app.conf.beat_schedule = {
    'once everyday':{
        'task':'tasks.update_doctor_wallet',
        'schedule': crontab(minute=15, hour=0),
        'args': (16,16)
    },
    'update release_date everyday':{
        'task':'tasks.update_sign_date',
        'schedule': crontab(minute=0, hour=0),
        'args': (16,16)
    },
    'update wallet everyday':{
        'task':'tasks.pay_to_wallet',
        'schedule': crontab(minute=30, hour=0),
        'args': (16,16)
    },
}

# Looks up for task modules in Django applications and loads them
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')