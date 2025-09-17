from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
import debug_toolbar
from debug_toolbar.toolbar import debug_toolbar_urls
from core.views import (LandingTemplateView, СontraindicationsTemplateView, ApplicationCreateView, ApplicationsListView, ApplicationDetailView, ApplicationUpdateView, ReviewCreateView, ThanksTemplateView, СontraindicationsTemplateView, ReviewsListView, ScheduleCreateView, SchedulesListView, ScheduleUpdateView, ScheduleDeleteView, get_schedule_by_coach)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", LandingTemplateView.as_view(), name="landing"),
    path("contraindications/", СontraindicationsTemplateView.as_view(), name="contraindications"),
    path("applications/", ApplicationsListView.as_view(), name="all-applications"),
    path("application/<int:application_id>/", ApplicationDetailView.as_view(), name="application"),
    path("application/create/", ApplicationCreateView.as_view(), name="application-create"),
    path("application/update/<int:application_id>/", ApplicationUpdateView.as_view(), name="application-update"),
    path("reviews/", ReviewsListView.as_view(), name="reviews"),
    path("review/create/", ReviewCreateView.as_view(), name="review-create"),
    path('schedule/create/', ScheduleCreateView.as_view(), name='schedule-create'),
    path('schedules/', SchedulesListView.as_view(), name='all-schedule'),
    path('schedule/<int:schedule_id>//', ScheduleUpdateView.as_view(), name='schedule-update'),
    path('schedule/delete/<int:schedule_id>//', ScheduleDeleteView.as_view(), name='schedule-delete'),
    path("thanks/<str:source>/", ThanksTemplateView.as_view(), name="thanks"),
    path('__debug__/', include(debug_toolbar.urls)),
        # AJAX вью для отдачи массива объектов услуг по ID мастера
    path("ajax/schedules/<int:coach_id>/", get_schedule_by_coach, name="get_schedule_by_coach"),
]

# Добавляем Статику и Медиа ЕСЛИ в режиме разработки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0]
    )
    # Подключим Django Debug  Toolbar

