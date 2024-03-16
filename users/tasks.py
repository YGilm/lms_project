# users/tasks.py

from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model

User = get_user_model()


@shared_task
def deactivate_inactive_users():
    time_interval = timezone.now() - timedelta(days=30)

    inactive_users = User.objects.filter(last_login__lt=time_interval, is_active=True)
    inactive_users.update(is_active=False)

    return inactive_users.count()

