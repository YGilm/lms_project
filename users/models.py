from django.contrib.auth.models import AbstractUser
from django.db import models

from materials.models import Course, Lesson

NULLABLE = {'null': True, 'blank': True}


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='почта')
    is_active = models.BooleanField(default=True)

    phone = models.CharField(max_length=35, verbose_name='телефон', **NULLABLE)
    city = models.CharField(max_length=50, verbose_name='город', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='аватар', **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


class Payment(models.Model):
    PAYMENT_METHOD = [('cash', 'наличные'), ('card', 'оплата картой')]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь')
    date_payment = models.DateField(verbose_name='дата платежа')
    course_paid = models.ForeignKey(Course, on_delete=models.SET_NULL, **NULLABLE, verbose_name='оплаченный курс')
    lesson_paid = models.ForeignKey(Lesson, on_delete=models.SET_NULL, **NULLABLE, verbose_name='оплаченный урок')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='сумма оплаты')
    payment_method = models.CharField(default='card', max_length=20, choices=PAYMENT_METHOD,
                                      verbose_name='способ оплаты')
    id_stripe_session = models.CharField(max_length=100, null=True, blank=True, verbose_name='id сессии stripe')
    is_succeed = models.BooleanField(default=False, verbose_name='оплата завершена')

    def __str__(self):
        return f'{self.id} плательщик: {self.user} сумма: {self.amount}'

    class Meta:
        verbose_name = 'платеж'
        verbose_name_plural = 'платежи'
