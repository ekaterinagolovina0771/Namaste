# users/mode
from django.db import models

# Импорт AbstractUser
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """
    Кастомная модель пользователя.
    Наследуясь от AbstractUser мы получаем все его поля и методы
    И можем быть интегрированы в Django гармонично
    """

    avatar = models.ImageField(
        upload_to="avatars", verbose_name="Аватар", null=True, blank=True
    )
    phone = models.CharField(
        max_length=20, verbose_name="Телефон", null=True, blank=True
    )
    birthday = models.DateField(verbose_name="Дата рождения", null=True, blank=True)
    vk_id = models.CharField(
        max_length=100, verbose_name="ID пользователя ВКонтакте", null=True, blank=True
    )
    tg_id = models.CharField(
        max_length=100, verbose_name="ID пользователя в Телеграм", null=True, blank=True
    )
    groups = models.ManyToManyField(
        'auth.Group',
        blank=True,
        related_name='custom_user_groups',  # Добавьте аргумент related_name
        related_query_name='custom_user',
        help_text='Группы, к которым принадлежит этот пользователь. Пользователь получит все разрешения, предоставленные каждой из его групп.',
        verbose_name='Группы',
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        blank=True,
        related_name='custom_user_permissions',  # Добавьте аргумент related_name
        related_query_name='custom_user',
        help_text='Определенные разрешения для этого пользователя.',
        verbose_name='Разрешения пользователя',
    )