from django.urls import reverse

def menu_items(request):
    """
    Контекстный процессор для добавления меню в контекст шаблонов.
    """
    menu = [
        {"title": "Главная", "url_name": "landing", "url": reverse("landing")},
        {
            "title": "About",
            "url": reverse("landing") + "#about",
        },
        {
            "title": "contraindications",
            "url": reverse("landing") + "#contraindications",
        },
        {
            "title": "Отзывы",
            "url": reverse("landing") + "#reviews",
        },
        {
            "title": "Записаться",
            "url": reverse("landing") + "#get-application",
        },
    ]

    menu_staff = [
        {"title": "Записи", "url": reverse("applications")},
        {"title": " Практики", "url": reverse("schedules")},
    ]

    return {"menu_items": menu, "menu_staff_items": menu_staff}
