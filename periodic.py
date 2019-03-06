from celery import Celery

from posting import process_posting

celery_settings = dict(broker='redis://redis:6379', result_backend='redis://redis:6379')

app = Celery('periodic', **celery_settings)

app.conf.beat_schedule = {
    "posting_to_social_network": {"task": "periodic.posting", "schedule": 10.0}
}


@app.task
def posting():
    print("Posting to social network!")
    process_posting()
