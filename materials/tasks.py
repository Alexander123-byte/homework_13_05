from celery import shared_task
from django.utils import timezone
from django.core.mail import send_mail
from materials.models import Course, Subscription
from datetime import timedelta


@shared_task
def send_course_update_notification(course_id):
    try:
        course = Course.objects.get(id=course_id)

        # Проверка времени последнего обновления
        if timezone.now() - course.last_updated < timedelta(hours=4):
            return

        # Подготовка и отправка уведомлений подписчикам
        subject = f'Курс {course.title} был обновлен'
        message = f'Курс "{course.title}" был обновлен. Проверьте новые материалы на нашем сайте.'

        subscriptions = Subscription.objects.filter(course=course)
        recipient_list = [subscription.user.email for subscription in subscriptions]

        send_mail(subject, message, 'noreply@example.com', recipient_list)

        # Обновление времени последнего обновления
        course.last_updated = timezone.now()
        course.save()

    except Course.DoesNotExist:
        pass
