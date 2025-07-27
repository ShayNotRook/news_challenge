import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "newsletter.settings")


app = Celery("newsletter")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()



app.conf.beat_schedule = {
    'scrape-every-10-minutes': {
        'task': '',
        'schedule': crontab(minute='*/10'),
    }
}