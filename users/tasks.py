from celery import shared_task
from django.utils.timezone import now, timedelta
from .models import User


@shared_task
def lock_inactive_users():
    inactive_period = timedelta(days=30)
    threshold_date = now() - inactive_period

    inactive_users = User.objects.filter(last_login__lte=threshold_date)

    for user in inactive_users:
        user.is_active = False
        user.save()
