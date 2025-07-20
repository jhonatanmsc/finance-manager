import os

from celery import Celery
from celery.schedules import crontab
from src.settings import TIME_ZONE

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.settings")
app = Celery("src")
app.conf.enable_utc = False
app.conf.update(timezone=TIME_ZONE)
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "store-supplier-contributions-summary": {
        "task": "goals.tasks.store_supplier_totals_summary",
        "schedule": crontab(minute="*/3"),
    },
}

app.conf.beat_schedule = {
    "store-goal-contributions-summary": {
        "task": "goals.tasks.store_goal_totals_summary",
        "schedule": crontab(minute="*/4"),
    },
}


@app.task(bind=True)
def debug_task(self):
    print("Request: {0!r}".format(self.request))
