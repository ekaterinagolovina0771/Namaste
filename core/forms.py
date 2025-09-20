from django import forms
from .models import Application, Review, Schedule, Coach
from django.utils import timezone
from datetime import datetime
from django.core.exceptions import ValidationError
from django.db.models import Subquery

class ReviewModelForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["name", "text", "rating", "coach"]
        widgets = {
            "text": forms.Textarea(attrs={"placeholder": "Ваш отзыв", "class": "form-control"}),
            "name": forms.TextInput(attrs={"placeholder": "Ваше имя", "class": "form-control"}),
            "rating": forms.Select(attrs={"placeholder": "Ваша оценка", "class": "form-control"}),
            "coach": forms.Select(attrs={"placeholder": "Ваш инструктор", "class": "form-select"}),
        }

class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = "__all__"
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Название практики"}
            ),
            "description": forms.Textarea(
                attrs={"placeholder": "Описание услуги", "class": "form-control"}
            ),
            "price": forms.NumberInput(attrs={"class": "form-control"}),
            'date': forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            'start_time': forms.TimeInput(attrs={'type': 'time', 'step': '300'}),
            "duration": forms.NumberInput(attrs={"class": "form-control"}),
        }
    coach = forms.ModelChoiceField(queryset=Coach.objects.all(), required=True)

    def clean_price(self):
        price = self.cleaned_data.get("price")
        if price < 0:
            raise forms.ValidationError("Цена не может быть отрицательной")
        return price

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ["name", "phone", "coach", "comment", "schedules"]
        widgets = {
            "name": forms.TextInput(
                attrs={"placeholder": "Ваше имя", "class": "form-control"}
            ),
            "phone": forms.TextInput(
                attrs={"placeholder": "+7 (999) 999-99-99", "class": "form-control"}
            ),
            "coach": forms.Select(attrs={"class": "form-select"}),
            "comment": forms.Textarea(
                attrs={
                    "placeholder": "Комментарий к заявке",
                    "class": "form-control",
                    "rows": 3,
                }
            ),
             "schedules": forms.CheckboxSelectMultiple(
                attrs={"class": "form-check-input"}
            ),
        }

   


    def clean_schedules(self):
        # Нам нужно добыть инструктора и все указанные практики из формы, добыть их из DB и проверить действительно ли инструктор назначил все эти практики

        schedules = self.cleaned_data.get("schedules")
        coach = self.cleaned_data.get("coach")

        if not coach:
            raise forms.ValidationError("Вы должны выбрать инструктора.")
        if not schedules:
            raise forms.ValidationError("Вы должны выбрать практику.")

        # Добывам все практики которые назначил этот инструктор на самом деле
        coach_schedules = coach.schedules.all()

        # Проверяем все ли практики которые выбрал пользователь назначил этот инструктор
        not_approved_schedules = []
        for schedule in schedules:
            if schedule not in coach_schedules:
                not_approved_schedules.append(schedule.name)

        if not_approved_schedules:
            raise forms.ValidationError("Этот инструктор не назначал следующие практики: " + ", ".join(not_approved_schedules))
        
        # Проверяем, не превышает ли количество выбранных расписаний установленное ограничение
        if len(schedules) > 1: 
            raise forms.ValidationError("Выберите одну практику.")
        
        # Check if the number of people attending each selected schedule exceeds the limit
        for schedule in schedules:
            if schedule.applications.filter(coach=self.cleaned_data.get("coach")).count() >= 8:
                raise forms.ValidationError("На это время все гамаки уже заняты. Вы можете записаться в резерв. Мы свяжемся с вами если места появятся.")
        
        return schedules



