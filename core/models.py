from django.db import models
from django.utils import timezone
from datetime import time, datetime

class Coach(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя')
    experience = models.TextField(blank=True, verbose_name='Опыт')
    photo = models.ImageField(upload_to='coach/', verbose_name='Изображение', null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тренер'
        verbose_name_plural = 'Тренеры'

class Practice(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Стоимость")
    duration = models.PositiveIntegerField(verbose_name="Продолжительность", help_text="Продолжительность практики в минутах", default=60)
    image = models.ImageField(upload_to='practices/', verbose_name='Изображение', null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Практика'
        verbose_name_plural = 'Практики'

class Schedule(models.Model):
    date = models.DateField(default=timezone.now)
    start_time = models.TimeField(default=time(9, 0))

    def __str__(self):
        return f"{self.date} {self.start_time}"
    class Meta:
        verbose_name = "Расписание"
        verbose_name_plural = "Расписание"

class Application(models.Model):
    STATUS_CHOICES = (
        ("new", "Новая"),
        ("confirmed", "Подтвержденная"),
        ("completed", "Завершеная"),
        ("canceled", "Отмененая"),
    )

    name = models.CharField(max_length=100, verbose_name="Имя")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    comment = models.CharField(max_length=500, null=True, blank=True, verbose_name="Комментарий")
    status = models.CharField(choices=STATUS_CHOICES, default="new", max_length=20, verbose_name="Статус")
    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name="Дата создания")
    date_updated = models.DateTimeField(auto_now=True, null=True, blank=True, verbose_name="Дата обновления")
    schedule = models.ForeignKey(Schedule, blank=True, null=True, on_delete=models.CASCADE)

    


    def __str__(self):
        return f"{self.name} - {self.phone}"

    class Meta:
        verbose_name = "Запись"
        verbose_name_plural = "Записи"

class Review(models.Model):
    RATING_CHOICES = [
        (1, "Ужасно"),
        (2, "Плохо"),
        (3, "Нормально"),
        (4, "Хорошо"),
        (5, "Отлично"),
    ]

    STATUS_CHOICES = [
        ("new", "Новый"),
        ("ai_moderating", "На модерации"),
        ("ai_approved", "Одобрен ИИ"),
        ("ai_rejected", "Отклонен ИИ"),
        ("published", "Опубликован"),
        ("archived", "В архиве"),
    ]

    name = models.CharField(max_length=50, verbose_name="Имя", blank=True, null=True)
    text = models.TextField(verbose_name="Текст отзыва")
    rating = models.PositiveSmallIntegerField(
        choices=RATING_CHOICES, verbose_name="Рейтинг", default=5
    )
    coach = models.ForeignKey(
        "Coach",
        on_delete=models.SET_NULL,
        related_name="reviews",
        verbose_name="Тренер",
        null=True,
        blank=True,
    )
    photo = models.ImageField(
        upload_to="reviews/", blank=True, null=True, verbose_name="Фото"
    )
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="new", verbose_name="Статус"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")




    def __str__(self):
        return f"{self.name} - {self.text}"

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"




