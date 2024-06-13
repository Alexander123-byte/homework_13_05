from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_update_email(subject, message, recipient_list):
    send_mail(
        subject,
        message,
        'san.juckov2017@yandex.ru',
        recipient_list,
        fail_silently=False,
    )
