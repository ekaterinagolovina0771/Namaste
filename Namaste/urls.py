from django.contrib import admin
from django.urls import path
from core.views import LandingTemplateView, ReviewCreateView, ThanksTemplateView, СontraindicationsTemplateView, ReviewsListView, ApplicationCreateView, ScheduleCreateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", LandingTemplateView.as_view(), name="landing"),
    path("contraindications/", СontraindicationsTemplateView.as_view(), name="contraindications"),
    # path("applications/", ApplicationsListView.as_view(), name="all_applications"),
    # path("application/<int:application_id>/", ApplicationDetailView.as_view(), name="application"),
    path("application/create/", ApplicationCreateView.as_view(), name="application-create"),
    # path("application/update/<int:application_id>/", ApplicationUpdateView.as_view(), name="application-update"),
    # path("application/delete/<int:application_id>/", ApplicationDeleteView.as_view(), name="application-delete"),
    path("review/create/", ReviewCreateView.as_view(), name="review-create"),
    path("reviews/list/", ReviewsListView.as_view(), name="reviews_list"),
    # path("contacts/", ContactsTemplateView.as_view(), name="contacts"),
    path("thanks/<str:source>/", ThanksTemplateView.as_view(), name="thanks"),
    path('schedule-create/', ScheduleCreateView.as_view(), name='schedule-create'),

]
