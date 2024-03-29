# Generated by Django 5.0.2 on 2024-03-11 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0003_subscription'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='last_update',
            field=models.DateTimeField(auto_now=True, verbose_name='последнее обновление'),
        ),
        migrations.AddField(
            model_name='course',
            name='price',
            field=models.PositiveIntegerField(default=0, verbose_name='цена'),
        ),
        migrations.AddField(
            model_name='course',
            name='stripe_id',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='id продукта на stripe.com'),
        ),
        migrations.AddField(
            model_name='lesson',
            name='last_update',
            field=models.DateTimeField(auto_now=True, verbose_name='последнее обновление'),
        ),
        migrations.AddField(
            model_name='lesson',
            name='price',
            field=models.PositiveIntegerField(default=0, verbose_name='цена'),
        ),
        migrations.AddField(
            model_name='lesson',
            name='stripe_id',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='id продукта на stripe.com'),
        ),
    ]
