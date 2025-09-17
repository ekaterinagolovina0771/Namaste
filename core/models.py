from django.db import models
from django.utils import timezone
from datetime import time, datetime

class Coach(models.Model):
    name = models.CharField(max_length=150, verbose_name="Имя", blank=True, null=True)
    photo = models.ImageField(upload_to="coaches", verbose_name="Фото", null=True, blank=True)
    phone = models.CharField(max_length=20, verbose_name="Телефон", blank=True, null=True)
    experience = models.PositiveIntegerField(verbose_name="Опыт работы", blank=True, null=True, default=0)
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    schedules = models.ManyToManyField("Schedule", verbose_name="Практики", default=None, related_name="coaches")
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Инструктор"
        verbose_name_plural = "Инструкторы"

        
    name = models.CharField(max_length=50, verbose_name="Название")
    description = models.TextField(blank=True, verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    


class Schedule(models.Model):
    name = models.CharField(max_length=50, verbose_name="Название", blank=True, null=True)
    date = models.DateField(default=timezone.now)
    start_time = models.TimeField(default=time(9, 0))
    duration = models.PositiveIntegerField(
    verbose_name="Длительность", help_text="Длительность практики в минутах", default=90)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Практика"
        verbose_name_plural = "Практики"


class Application(models.Model):
    STATUS_CHOICES = (
        ("new", "Новая"),
        ("confirmed", "Подтвержденная"),
        ("completed", "Завершенная"),
        ("canceled", "Отмененная"),
        ( "reserve", "Резерв")
    )

    name = models.CharField(max_length=100, verbose_name="Имя")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    comment = models.CharField(max_length=500, null=True, blank=True, verbose_name="Комментарий")
    status = models.CharField(choices=STATUS_CHOICES, default="new", max_length=20, verbose_name="Статус")
    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name="Дата создания")
    date_updated = models.DateTimeField(auto_now=True, null=True, blank=True, verbose_name="Дата обновления")
    coach = models.ForeignKey("Coach", on_delete=models.SET_NULL, null=True, verbose_name="Инструктор")
    schedule = models.ManyToManyField("Schedule", verbose_name="Практики",  default=None, related_name="applications")

    def __str__(self):
        return f"{self.name} - {self.phone}" if self.name and self.phone else "Не указано имя или номер телефона"

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
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="new", verbose_name="Статус"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")




    def __str__(self):
        return f"{self.name} - {self.text}"

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"




