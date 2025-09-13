from django.contrib import admin
from django.urls import path
from core.views import base

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", base),
    # path("", LandingTemplateView.as_view(), name="landing"),
    # path("about/", AboutTemplateView.as_view(), name="about"),
    # path("practices/", practicesTemplateView.as_view(), name="practices"),
    # path("practice/<int:practice_id>/", practiceDetailView.as_view(), name="practice"),
    # path("practice/create/", practiceCreateView.as_view(), name="practice-create"),
    # path("practice/update/<int:practice_id>/", practiceUpdateView.as_view(), name="practice-update"),
    # path("practice/delete/<int:practice_id>/", practiceDeleteView.as_view(), name="practice-delete"),
    # path("book_practice/", BookpracticeTemplateView.as_view(), name="book_practice"),
    # path("applications/", ApplicationsListView.as_view(), name="all_applications"),
    # path("application/<int:application_id>/", ApplicationDetailView.as_view(), name="application"),
    # path("application/create/", ApplicationCreateView.as_view(), name="application-create"),
    # path("application/update/<int:application_id>/", ApplicationUpdateView.as_view(), name="application-update"),
    # path("application/delete/<int:application_id>/", ApplicationDeleteView.as_view(), name="application-delete"),
    # path("review/create/", ReviewCreateView.as_view(), name="review-create"),
    # path("contacts/", ContactsTemplateView.as_view(), name="contacts"),
    # path("instructor/", InstructorTemplateView.as_view(), name="instructor"),
    # path("thanks/", ThanksTemplateView.as_view(), name="thanks"),
]
