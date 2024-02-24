from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):

        user = User.objects.create(
            email=input('email: '),
            first_name=input('first_name: '),
            last_name=input('last_name: '),
            is_superuser=bool(input('is_superuser (yes/no): ').lower() == 'yes'),
            is_staff=bool(input('is_staff (yes/no): ').lower() == 'yes'),
            phone=(input('phone: ')),
            city=(input('city: ')),
            is_active=True
        )

        user.set_password('0071')
        user.save()
