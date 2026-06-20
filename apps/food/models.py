from django.db import models


class Dish(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    photo = models.ImageField(upload_to='dishes/', blank=True, null=True)

    # КБЖУ на 100 грамм
    calories_per_100g = models.PositiveIntegerField(default=0)
    protein_per_100g = models.FloatField(default=0.0)
    fat_per_100g = models.FloatField(default=0.0)
    carbs_per_100g = models.FloatField(default=0.0)

    class Meta:
        verbose_name = 'Блюдо'
        verbose_name_plural = 'Блюда'

    def __str__(self):
        return self.name


class Ration(models.Model):
    TAG_CHOICES = [
        ('slim', 'Похудение (1200-1400 ккал)'),
        ('balance', 'Поддержание (1600-1800 ккал)'),
        ('strong', 'Набор массы (2000+ ккал)'),
    ]

    name = models.CharField(max_length=100)
    calories_tag = models.CharField(max_length=20, choices=TAG_CHOICES, db_index=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    dishes = models.ManyToManyField('Dish', through='RationDish')

    class Meta:
        verbose_name = 'Рацион'
        verbose_name_plural = 'Рационы'

    def __str__(self):
        return f"{self.name} ({self.get_calories_tag_display()})"


class RationDish(models.Model):
    DAY_CHOICES = [
        (1, 'День 1 (Понедельник)'),
        (2, 'День 2 (Вторник)'),
        (3, 'День 3 (Среда)'),
        (4, 'День 4 (Четверг)'),
        (5, 'День 5 (Пятница)'),
    ]

    ration = models.ForeignKey(Ration, on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    weight = models.PositiveIntegerField()
    day_number = models.PositiveSmallIntegerField(choices=DAY_CHOICES, default=1)

    class Meta:
        verbose_name = 'Блюдо в рационе'
        verbose_name_plural = 'Блюда в рационах'
        unique_together = ('ration', 'dish', 'day_number')

    def __str__(self):
        return f"День {self.day_number} | {self.dish.name} ({self.weight}г) → {self.ration.name}"

    # Автоматически считает калории для этой порции
    @property
    def total_calories(self):
        return round(self.dish.calories_per_100g * self.weight / 100)

    @property
    def total_protein(self):
        return round(self.dish.protein_per_100g * self.weight / 100, 1)

    @property
    def total_fat(self):
        return round(self.dish.fat_per_100g * self.weight / 100, 1)

    @property
    def total_carbs(self):
        return round(self.dish.carbs_per_100g * self.weight / 100, 1)