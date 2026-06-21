from django.db import models

# users/models.py
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    # Добавляем кастомные поля для твоего фитнес-приложения
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Телефон")
    weight = models.FloatField(blank=True, null=True, verbose_name="Вес (кг)")
    height = models.FloatField(blank=True, null=True, verbose_name="Рост (см)")
    
    # Можно сразу добавить уровень активности для расчёта калорий в будущем
    # ACTIVITY_CHOICES = [
    #     ('low', 'Низкая'),
    #     ('medium', 'Средняя'),
    #     ('high', 'Высокая'),
    # ]
    # activity = models.CharField(max_length=10, choices=ACTIVITY_CHOICES, default='medium')

    def __str__(self):
        return self.username
