from django.db import models
from config import settings

NULLABLE = {'null': True, 'blank': True}


class Course(models.Model):
    title = models.CharField(max_length=150, verbose_name='название')
    image = models.ImageField(upload_to='materials/', verbose_name='изображение', **NULLABLE)
    description = models.TextField(verbose_name='описание')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='courses', **NULLABLE)
    price = models.PositiveIntegerField(default=0, verbose_name='цена')
    stripe_price_id = models.CharField(max_length=100, null=True, blank=True, verbose_name='id цены в stripe')
    stripe_id = models.CharField(max_length=50, verbose_name='id продукта на stripe.com', **NULLABLE)
    last_update = models.DateTimeField(auto_now=True, verbose_name='последнее обновление')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons', verbose_name='курс')
    title = models.CharField(max_length=150, verbose_name='название')
    description = models.TextField(verbose_name='описание')
    image = models.ImageField(upload_to='materials/', verbose_name='изображение', **NULLABLE)
    video_url = models.URLField(verbose_name='ссылка на видео', **NULLABLE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='lessons', **NULLABLE)
    price = models.PositiveIntegerField(default=0, verbose_name='цена')
    stripe_price_id = models.CharField(max_length=100, verbose_name='id цены в stripe', **NULLABLE)
    stripe_id = models.CharField(max_length=50, verbose_name='id продукта на stripe.com', **NULLABLE)
    last_update = models.DateTimeField(auto_now=True, verbose_name='последнее обновление')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'


class Subscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='subscriptions')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='subscribers')

    class Meta:
        unique_together = ('user', 'course')
        verbose_name = 'подписка'
        verbose_name_plural = 'подписки'

    def __str__(self):
        return f'{self.user} подписан на курс {self.course.title}'
