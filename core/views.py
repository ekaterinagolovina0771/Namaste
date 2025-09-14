# core/views.py
from .forms import ReviewModelForm, ApplicationForm, ScheduleForm
from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse, HttpResponseNotAllowed
from django.core.exceptions import ValidationError
from django.contrib import messages
from .models import Coach, Practice, Application, Review, Schedule
# from .forms import PracticeForm, ApplicationForm, ReviewModelForm
from django.db.models import Q, Count, Sum, F
# Импорт миксинов для проверки прав
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin

# Импорт классовых вью, View, TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views import View
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView,
)
from django.urls import reverse_lazy


class LandingTemplateView(TemplateView):
    template_name = "landing.html"

class ReviewCreateView(CreateView):
    model = Review
    form_class = ReviewModelForm
    template_name = "review_class_form.html"
    success_url = reverse_lazy("thanks", kwargs={"source": "review-create"})

class ThanksTemplateView(TemplateView):
    """
    Классовая view для маршрута 'thanks/'
    """

    template_name = "thanks.html"

    def get_context_data(self, **kwargs):
        """
        Расширение get_context_data для возможности передать в шаблон {{ title }} и {{ message }}.

        Они будут разные, в зависимости от куда пришел человек.
        Со страницы order/create/ с псевдонимом order-create
        Или со страницы review/create/ с псевдонимом review-create
        """
        context = super().get_context_data(**kwargs)

        if kwargs["source"]:
            source = kwargs["source"]
            if source == "application-create":
                context["title"] = "Спасибо!"
                context["message"] = (
                    "Вы записаны! Мы напомним Вам о предстоящей тренировке."
                )
            elif source == "review-create":
                context["title"] = "Спасибо за отзыв!"
                context["message"] = (
                    "Ваш отзыв принят и отправлен на модерацию. После проверки он появится на сайте."
                )
            elif source == "schedule-create":
                context["title"] = "Спасибо!"
                context["message"] = (
                    "Тренировка назначена"
                )

        else:
            context["title"] = "Спасибо!"
            context["message"] = "Спасибо за ваше обращение!"

        return context

class СontraindicationsTemplateView(TemplateView):
    template_name = "contraindications.html"

class ReviewsListView(ListView):
    template_name = "reviews_list.html"
    model = Review
    context_object_name = "reviews"

class ApplicationCreateView(CreateView):
    form_class = ApplicationForm
    template_name = "application_class_form.html"
    success_url = reverse_lazy("thanks", kwargs={"source": "application-create"})
   
class ScheduleСreateView(CreateView):
    form_class = ScheduleForm
    template_name = "schedule_class_form.html"
    success_url = reverse_lazy("thanks", kwargs={"source": "schedule-create"})