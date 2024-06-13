from celery import shared_task
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from .models import User


@shared_task
def lock_inactive_users():
    now = timezone.now()
    month_ago = now - relativedelta(months=1)
    qs = User.objects.filter(last_login__lt=month_ago, is_active=True)
    qs.update(is_active=False)
