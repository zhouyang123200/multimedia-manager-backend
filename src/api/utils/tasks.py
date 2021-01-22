from celery import Celery

celery = Celery(__name__)

@celery.task()
def add_together(a, b):
    return a + b

