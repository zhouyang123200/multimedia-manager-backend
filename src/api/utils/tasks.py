from celery import Celery
from flask_mail import Message
from flask import current_app

celery = Celery(__name__)

@celery.task()
def add_together(a, b):
    return a + b

@celery.task()
def send_mail(subject, sender, recipients:list, text):
    msg = Message(subject=subject, sender=sender, recipients=recipients, body=text)
    current_app.mail.send(msg)
    current_app.logger.info('send email successfully')

