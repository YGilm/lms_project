# Generated by Django 5.0.2 on 2024-03-13 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_payment_date_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='payment_url',
            field=models.URLField(blank=True, max_length=255, null=True, verbose_name='ссылка на оплату'),
        ),
    ]
