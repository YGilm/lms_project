from celery import shared_task
from django.core.mail import send_mail
from django.db.models import Q
from .models import Course, Subscription, Lesson


@shared_task
def send_update_email(object_id, model_name):
    if model_name == 'course':
        model = Course.objects.get(id=object_id)
        subscriptions = Subscription.objects.filter(course=model)
    else:
        model = Lesson.objects.get(id=object_id)
        subscriptions = Subscription.objects.filter(course=model.course)

    subject = f'Обновление {model_name}: {model.title}'
    message = f'Привет! {model_name.capitalize()} "{model.title}" был обновлен.'
    emails = subscriptions.values_list('user__email', flat=True)

    send_mail(
        subject,
        message,
        from_email='admin@example.com',
        recipient_list=list(emails),
        fail_silently=False,
    )
