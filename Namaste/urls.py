from django.contrib import admin
from django.urls import path
from core.views import LandingTemplateView, СontraindicationsTemplateView, ApplicationCreateView, ApplicationsListView, ApplicationDetailView, ApplicationUpdateView, ReviewCreateView, ThanksTemplateView, СontraindicationsTemplateView, ReviewsListView, ScheduleCreateView, SchedulesListView, ScheduleUpdateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", LandingTemplateView.as_view(), name="landing"),
    path("contraindications/", СontraindicationsTemplateView.as_view(), name="contraindications"),
    path("applications/", ApplicationsListView.as_view(), name="all_applications"),
    path("application/<int:application_id>/", ApplicationDetailView.as_view(), name="application"),
    path("application/create/", ApplicationCreateView.as_view(), name="application-create"),
    path("application/update/<int:application_id>/", ApplicationUpdateView.as_view(), name="application-update"),
    path("reviews/", ReviewsListView.as_view(), name="reviews"),
    path("review/create/", ReviewCreateView.as_view(), name="review-create"),
    path('schedule/create/', ScheduleCreateView.as_view(), name='schedule-create'),
    path('schedules/', SchedulesListView.as_view(), name='all_schedule'),
    path('schedule/<int:schedule_id>//', ScheduleUpdateView.as_view(), name='schedule-update'),
    path("thanks/<str:source>/", ThanksTemplateView.as_view(), name="thanks"),





]
