# core/views.py
from django.forms import BaseModelForm
from .forms import ReviewModelForm, ApplicationForm, ScheduleForm
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseNotAllowed, HttpResponseRedirect, HttpResponse, Http404
from django.core.exceptions import ValidationError
from django.contrib import messages
from .models import Application, Review, Schedule, Coach
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
from django.urls import reverse_lazy, reverse


class UserIsStuffPassedMixin(UserPassesTestMixin):
    """
    Миксин для проверки, является ли пользователь персоналом сайта
    """
    def test_func(self):
        """
        Метод от ответа которого будет зависеть доступ к вью
        """
        return self.request.user.is_staff

class AjaxCoachSchedulesView(View):
    """
    Вью для отдачи массива объектов практик по ID инструктора.
    Обслуживает AJAX запросы формы создания заказа.
    """
    def get(self, request, coach_id):
        coach = Coach.objects.prefetch_related("schedules").get(id=coach_id)
        schedules = coach.schedules.all()

        schedules_data = [{"id": schedule.id, "name": schedule.name} for schedule in schedules]

        return JsonResponse({"schedules": schedules_data})

class ReviewCreateView(CreateView):
    model = Review
    form_class = ReviewModelForm
    template_name = "review_class_form.html"
    success_url = reverse_lazy("thanks", kwargs={"source": "review-create"})


class LandingTemplateView(TemplateView):
    """Классовая view для главной страницы"""

    template_name = "landing.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["coaches"] = Coach.objects.prefetch_related("schedules").annotate(
            num_schedules=Count("schedules")
        )
        context["schedules"] = Schedule.objects.all()
        context["reviews"] = Review.objects.all()

        return context

class ThanksTemplateView(TemplateView):
    """
    Классовая view для маршрута 'thanks/'
    """

    template_name = "thanks.html"

    def get_context_data(self, **kwargs):
        """
        Расширение get_context_data для возможности передать в шаблон {{ title }} и {{ message }}.

        Они будут разные, в зависимости от куда пришел человек.
        Со страницы application/create/ с псевдонимом application-create
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


class ApplicationsListView(UserIsStuffPassedMixin, ListView):
    model = Application
    template_name = "applications_list.html"
    context_object_name = "applications"
    # Помещает объект с назваем page_obj в контекст шаблона
    paginate_by = 20

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
        applications = (
            queryset.prefetch_related("schedules")
            .select_related("coach")
            .filter(search_q & status_q)
            .order_by(ordering)
        )

        return applications
    
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



class SchedulesListView(UserIsStuffPassedMixin, ListView):
    model = Schedule
    template_name = "schedules_list.html"
    context_object_name = "schedules"
    # Помещает объект с назваем page_obj в контекст шаблона
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        # Получаю из GET запроса все данные URL
        # ПОИСКОВАЯ ФОРМА
        search_query = self.request.GET.get("q", "")
        # ЧЕКБОКСЫ выборки по полям
        # 1. поиск по дате - search_by_date

        checkbox_date = self.request.GET.get("search_by_date", "")

        # РАДИОКНОПКА Порядок сортировки по дате
        # order_by_date - desc, asc
        order_by_date = self.request.GET.get("order_by_date", "desc")

        # 1. Создаем Q-объект для текстового поиска
        search_q = Q()
        if search_query:
            # Внутренние условия поиска объединяем через ИЛИ (|=)
            if checkbox_date:
                search_q |= Q(date__icontains=search_query)


        # Порядок сортировки
        ordering = "-date" if order_by_date == "desc" else "date"

        # 3. Объединяем два Q-объекта через И (&)
        # Это гарантирует, что запись должна соответствовать И условиям поиска, И условиям статуса
        schedules = (queryset.filter(search_q).order_by(ordering))

        return schedules

class ApplicationDetailView(UserIsStuffPassedMixin, DetailView):
    model = Application
    template_name = "application_detail.html"
    context_object_name = "application"
    pk_url_kwarg = "application_id"  # Указываем, что id брать из URL kwarg 'application_id'

    def get_queryset(self):
        """
        Лучшее место для "жадной" загрузки и аннотаций.
        Этот метод подготавливает оптимизированный QuerySet.
        """
        queryset = super().get_queryset()
        return (
            queryset.select_related("coach")
            .prefetch_related("schedules")
            .annotate(total_price=Sum("schedules__price"))
        )

    def get_object(self, queryset=None):
        """
        Лучшее место для логики, специфичной для одного объекта.
        Например, для счетчика просмотров.
        """
        # Сначала получаем объект стандартным способом (он будет взят из queryset,
        # который мы определили в get_queryset)
        application = super().get_object(queryset)

        # Теперь выполняем логику с сессией и счетчиком
        session_key = f"application_{application.id}_viewed"
        if not self.request.session.get(session_key):
            self.request.session[session_key] = True
            # Атомарно увеличиваем счетчик в БД
            application.view_count = F("view_count") + 1
            application.save(update_fields=["view_count"])
            # Обновляем объект из БД, чтобы в шаблоне было актуальное значение
            application.refresh_from_db()

        return application
    
class ApplicationCreateView(CreateView):
    form_class = ApplicationForm
    template_name = "application_class_form.html"
    success_url = reverse_lazy("thanks", kwargs={"source": "application-create"})
    success_message = "Вы записаны на практику!"

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        messages.success(self.request, self.success_message)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["operation_type"] = "Запись на практику"
        return context
    
class ApplicationUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = "core.change_application"
    model = Application
    form_class = ApplicationForm
    template_name = "application_class_form.html"
    success_url = reverse_lazy("applications")
    success_message = "Запись успешно обновлена!"
    pk_url_kwarg = "application_id"

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        messages.success(self.request, self.success_message)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["operation_type"] = "Редактирование записи"
        return context



class ReviewsListView(UserIsStuffPassedMixin, ListView):
    template_name = "reviews_list.html"
    model = Review
    context_object_name = "reviews"

class ScheduleCreateView(UserIsStuffPassedMixin, CreateView):
    form_class = ScheduleForm
    template_name = "schedule_class_form.html"
    success_url = reverse_lazy("schedule")
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["operation_type"] = "Назначение практики"
        return context

    def form_valid(self, form):
        # get the selected coach
        coach = form.cleaned_data.get('coach')

        # create a new Schedule instance
        schedule_data = {'coach': coach, **form.cleaned_data}
        schedule = Schedule.objects.create(**schedule_data)

        # Associate the schedule with the coach
        coach.schedules.add(schedule)

        messages.success(self.request, "Практика успешно назначена!")
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        messages.error(self.request, "Ошибка валидации формы! Проверьте введенные данные.")
        return super().form_invalid(form)

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj is None:
            raise Http404("No Schedule found with this id.")
        return obj

    def get_success_url(self):
        if self.object:
            return reverse('schedule-update', kwargs={'pk': self.object.pk})
        else:
            return self.success_url
            
class ScheduleUpdateView(UserIsStuffPassedMixin, UpdateView):
    model = Schedule
    form_class = ScheduleForm
    template_name = "schedule_class_form.html"
    success_url = reverse_lazy("schedule")
    # Стандартное имя - pk, если в url другое - мы можем дать название тут
    pk_url_kwarg = "schedule_id"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["operation_type"] = "Редактирование практики"
        return context
    
    def form_valid(self, form):
        messages.success(self.request, "Практика успешно обновлена!")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "Ошибка валидации формы! Проверьте введенные данные.")
        return super().form_invalid(form)