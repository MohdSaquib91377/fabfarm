from django.core import mail
from django.conf import settings
from celery import shared_task

@shared_task(name="send_mail")
def send_mail(subject:str, body:str,to_email:str) ->None :
    mail.send_mail(subject, body,settings.EMAIL_HOST_USER,to_email,fail_silently=False)
