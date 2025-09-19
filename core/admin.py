from typing import Any
from django.contrib import admin
from django.db.models import QuerySet, Sum
from .models import Application, Review, Schedule, Coach

# admin.site.register(Application)
# admin.site.register(Review)
# admin.site.register(Schedule)
# admin.site.register(Coach)


# Делаем красивый вариант для Application
@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):

    # Отображение полей в списке
    list_display = (
        "name",
        "phone",
        "coach",
        "comment",
        "status",
        "date_created",
        "date_updated",
    )

    # Поисковая форма
    search_fields = ("name", "phone", "comment")

    # Фильтрация
    list_filter = ("status", "coach")

    # Сколько записей на странице
    list_per_page = 20

    # Кликабельные поля
    list_display_links = ("phone", "name")

    # Поля, которые можно редактировать
    list_editable = ("status",)

    # НЕ редактируемые поля в детальном просмотре (выводит автонаполняемые поля, убирает возможность редактирования если надо)
    readonly_fields = ("date_created", "date_updated")

    # Регистрация действий
    actions = ("mark_completed", "mark_canceled", "mark_new", "mark_confirmed", "mark_reserve")

   # Удобное отоброжение M2M услуг в детальном отображении
    filter_horizontal = ("schedules",)

    # Группируем поля на странице редактирования
    fieldsets = (
        ("Основная информация", {"fields": ("name", "phone", "status", "comment")}),
        (
            "Служебная информация (только для чтения)",
            {"classes": ("collapse",), "fields": ("date_created", "date_updated")},
        ),
    )

    # Кастомное действие - отметить заявки как completed - Завершена
    @admin.action(description="Отметить как завершенные")
    def mark_completed(self, request, queryset):
        queryset.update(status="completed")

    @admin.action(description="Отметить как отмененные")
    def mark_canceled(self, request, queryset):
        queryset.update(status="canceled")

    @admin.action(description="Отметить как новые")
    def mark_new(self, request, queryset):
        queryset.update(status="new")

    @admin.action(description="Отметить как подтвержденные")
    def mark_confirmed(self, request, queryset):
        queryset.update(status="confirmed")

    @admin.action(description="Отметить как зарезервированные")
    def mark_reserve(self, request, queryset):
        queryset.update(status="reserved")

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):

    # Отображение полей в списке
    list_display = ["name", "coach", "rating", "status", "created_at"]
    # Поисковая форма
    search_fields = ["coach", "comment"]
    # Фильтрация
    list_filter = ["coach", "status", "rating"]
    # Сколько записей на странице
    list_per_page = 10
    # Кликабельные поля
    list_display_links = ["name"]
    # Поля, которые можно редактировать
    list_editable = ["status"]
    # Регистрация действий
    actions = ["check_published"]


    @admin.action(description="Опубликовать отзыв")
    def check_published(self, request, queryset):
        queryset.update(status="published")
    


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):

    # Отображение полей в списке
    list_display = (
        "date",
        "start_time",
    )

   # Кликабельные поля
    list_display_links = ["date"]

    # Фильтрация
    list_filter = ("date", "start_time")

    # Сколько записей на странице
    list_per_page = 30

@admin.register(Coach)
class CoachAdmin(admin.ModelAdmin):

    # Отображение полей в списке
    list_display = ("name", "phone", "experience", "is_active", "get_schedules")
    def get_schedules(self, obj):
        return ", ".join([s.name for s in obj.schedules.all()])
    get_schedules.short_description = 'Schedules'






