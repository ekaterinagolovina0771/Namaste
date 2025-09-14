# core/views.py
from .forms import ReviewModelForm, ApplicationForm, ScheduleForm
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseNotAllowed
from django.core.exceptions import ValidationError
from django.contrib import messages
from .models import Application, Review, Schedule
# from .forms import ApplicationForm, ReviewModelForm
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

class СontraindicationsTemplateView(TemplateView):
    template_name = "contraindications.html"

class ApplicationsListView(ListView):
    model = Application
    template_name = "applications_list.html"
    context_object_name = "applications"
    # Помещает объект с назваем page_obj в контекст шаблона
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        # Получаю из GET запроса все данные URL
        # ПОИСКОВАЯ ФОРМА
        search_query = self.request.GET.get("q", "")
        # ЧЕКБОКСЫ выборки по полям
        # 1. поиск по телефону - search_by_phone
        # 2. поиск по имени - search_by_name
        # 3. поиск по тексту комментария - search_by_comment
        checkbox_name = self.request.GET.get("search_by_name", "")
        checkbox_phone = self.request.GET.get("search_by_phone", "")
        checkbox_comment = self.request.GET.get("search_by_comment", "")
        # ЧЕКББОКСЫ выборки по статусам
        # status_new
        # status_confirmed
        # status_completed
        # status_canceled
        checkbox_status_new = self.request.GET.get("status_new", "")
        checkbox_status_confirmed = self.request.GET.get("status_confirmed", "")
        checkbox_status_completed = self.request.GET.get("status_completed", "")
        checkbox_status_canceled = self.request.GET.get("status_canceled", "")
        checkbox_status_reserved = self.request.GET.get("status_reserved", "")

        # РАДИОКНОПКА Порядок сортировки по дате
        # order_by_date - desc, asc
        order_by_date = self.request.GET.get("order_by_date", "desc")

        # 1. Создаем Q-объект для текстового поиска
        search_q = Q()
        if search_query:
            # Внутренние условия поиска объединяем через ИЛИ (|=)
            if checkbox_phone:
                search_q |= Q(phone__icontains=search_query)
            if checkbox_name:
                search_q |= Q(name__icontains=search_query)
            if checkbox_comment:
                search_q |= Q(comment__icontains=search_query)

        # 2. Создаем Q-объект для фильтрации по статусам
        status_q = Q()
        # Условия статусов тоже объединяем через ИЛИ (|=)
        if checkbox_status_new:
            status_q |= Q(status="new")
        if checkbox_status_confirmed:
            status_q |= Q(status="confirmed")
        if checkbox_status_completed:
            status_q |= Q(status="completed")
        if checkbox_status_canceled:
            status_q |= Q(status="canceled")
        if checkbox_status_reserved:
            status_q |= Q(status="reserved")

        # Порядок сортировки
        ordering = "-date_created" if order_by_date == "desc" else "date_created"

        # 3. Объединяем два Q-объекта через И (&)
        # Это гарантирует, что запись должна соответствовать И условиям поиска, И условиям статуса
        orders = (queryset.filter(search_q & status_q).order_by(ordering))

        return orders
    
    def get_context_data(self, **kwargs):
        """
        Добавляем в контекст параметры GET-запроса для корректной работы пагинации с фильтрами.
        """
        context = super().get_context_data(**kwargs)
        # Копируем текущие GET-параметры
        get_params = self.request.GET.copy()
        # Если в параметрах есть 'page', мы его удаляем,
        # так как номер страницы будет добавлен в шаблоне
        if 'page' in get_params:
            del get_params['page']
        # Кодируем параметры в строку и добавляем в контекст
        context['get_params'] = get_params.urlencode()
        return context


class ReviewsListView(ListView):
    model = Review
    template_name = "reviews.html"
    context_object_name = "reviews"

class SchedulesListView(ListView):
    model = Schedule
    template_name = "schedule_list.html"
    context_object_name = "schedules"


class ApplicationDetailView(DetailView):
    model = Application
    template_name = "application_detail.html"
    context_object_name = "application"
    pk_url_kwarg = "application_id"

    def get_object(self, queryset=None):
        application_id = self.kwargs.get(self.pk_url_kwarg)
        return get_object_or_404(Application, pk=application_id)



class ScheduleUpdateView(UpdateView):
    model = Schedule
    form_class = ScheduleForm
    template_name = "schedule_form.html"
    success_url = reverse_lazy("schedules")



class ApplicationUpdateView(UpdateView):
    model = Application
    form_class = ApplicationForm
    template_name = "application_class_form.html"
    success_url = reverse_lazy("applications")



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



class ReviewsListView(ListView):
    template_name = "reviews_list.html"
    model = Review
    context_object_name = "reviews"

class ApplicationCreateView(CreateView):
    form_class = ApplicationForm
    template_name = "application_class_form.html"
    success_url = reverse_lazy("thanks", kwargs={"source": "application-create"})

    def form_valid(self, form):
        # Получите расписание из формы
        schedule_id = self.request.POST.get('schedule')
        schedule = Schedule.objects.get(pk=schedule_id)

        # Проверьте количество записей на расписание
        if schedule.application_set.count() >= 10:
            # Если достигнуто максимальное количество записей, отобразите сообщение об ошибке
            form.add_error('schedule', 'Все гамаки на это время заняты. Вы можете записаться в резерв или выбрать другое удобное для Вас время.')
            return self.form_invalid(form)
        
        # Если есть свободные места, продолжайте обработку формы
        form.instance.schedule = schedule
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['initial'] = {'schedule': self.get_initial_schedule()}
        return kwargs

    def get_initial_schedule(self):
        # Получите расписание для выбора клиентом
        schedule = Schedule.objects.first()  # Замените на вашу логику получения расписания
        return schedule.pk

    def get_selected_schedule(self):
        # Получите выбранное расписание из формы
        schedule_id = self.request.POST.get('schedule')
        schedule = Schedule.objects.get(pk=schedule_id)
        return schedule
    
    



class ScheduleCreateView(CreateView):
    form_class = ScheduleForm
    template_name = "schedule_class_form.html"
    success_url = reverse_lazy("thanks", kwargs={"source": "schedule-create"})
    def get_selected_schedule(self):
        # Получите выбранное расписание из формы
        schedule_id = self.request.POST.get('schedule')
        try:
            schedule = Schedule.objects.get(pk=schedule_id)
        except Schedule.DoesNotExist:
            # Обработайте случай, когда объект Schedule не существует
            # Например, вы можете вызвать исключение или вернуть значение по умолчанию
            raise Http404("Расписание, соответствующее запросу, не существует.")
        return schedule