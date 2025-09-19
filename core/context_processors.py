# core/context_processors.py
from django.urls import reverse


def menu_items(request):
    """
    Контекстный процессор для добавления меню в контекст шаблонов.
    """

    menu = [
        {
            "name": "Главная",
            "url": reverse("landing") + "#top",
            "icon_class": "bi-house",
        },
                {
            "name": "Инструкторы",
            "url": reverse("landing") + "#coaches",
            "icon_class": "bi-person-badge",
        },
        {
            "name": "О практиках",
            "url": reverse("landing") + "#about",
            "icon_class": "bi-person-badge",
        },
        {
            "name": "contraindications",
            "url": reverse("landing") + "#contraindications",
            "icon_class": "bi-scissors",
        },
        {
            "name": "Отзывы",
            "url": reverse("landing") + "#reviews",
            "icon_class": "bi-chat-dots",
        },
        {
            "name": "Записаться",
            "url": reverse("landing") + "#application-create",
            "icon_class": "bi-calendar-check",
        },
    ]

    staff_menu = [
        {
            "name": "Записи",
            "url": reverse("applications"),
            "icon_class": "bi-clipboard-data",
        },
        {
            "name": "Практики",
            "url": reverse("schedule"),
            "icon_class": "bi-list-check",
        },
    ]

    return {"menu_items": menu, "menu_staff_items": staff_menu}
