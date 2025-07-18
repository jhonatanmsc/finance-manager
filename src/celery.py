from celery import Celery
from celery.schedules import crontab

app = Celery("src")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print("Request: {0!r}".format(self.request))


app.conf.beat_schedule = {
    "print-message-ten-seconds": {
        "task": "store_supplier_sales_summary",
        "schedule": crontab(minute="*"),
    },
}
