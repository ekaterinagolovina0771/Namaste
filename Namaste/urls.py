from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from debug_toolbar.toolbar import debug_toolbar_urls
from core.views import (LandingTemplateView,  ApplicationCreateView, ApplicationsListView, ApplicationDetailView, ApplicationUpdateView, ReviewCreateView, ThanksTemplateView, ReviewsListView, ScheduleCreateView, SchedulesListView, ScheduleUpdateView, AjaxCoachSchedulesView)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", LandingTemplateView.as_view(), name="landing"),
    path("applications/", ApplicationsListView.as_view(), name="applications"),
    path("application/<int:application_id>/", ApplicationDetailView.as_view(), name="application"),
    path("application/create/", ApplicationCreateView.as_view(), name="application-create"),
    path("application/update/<int:application_id>/", ApplicationUpdateView.as_view(), name="application-update"),
    path("reviews/", ReviewsListView.as_view(), name="reviews"),
    path("review/create/", ReviewCreateView.as_view(), name="review-create"),
    path('schedule/create/', ScheduleCreateView.as_view(), name='schedule-create'),
    path('schedules/', SchedulesListView.as_view(), name='schedule'),
    path('schedule/update/<int:schedule_id>/', ScheduleUpdateView.as_view(), name='schedule-update'),
    path("thanks/<str:source>/", ThanksTemplateView.as_view(), name="thanks"),
    
    # AJAX вью для отдачи массива объектов услуг по ID мастера
    path("ajax/schedules/<int:coach_id>/", AjaxCoachSchedulesView.as_view(), name="get_schedule_by_coach"),
    
    # Подключаем маршруты приложения users
    path("users/", include("users.urls")),
]

# Добавляем Статику и Медиа ЕСЛИ в режиме разработки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    # Подключим Django Debug  Toolbar
        # Подключим Django Debug Toolbar
    urlpatterns += debug_toolbar_urls()

