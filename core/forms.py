from django import forms
from .models import Application, Review, Schedule, Coach
from django.utils import timezone
from datetime import datetime


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

    def clean_price(self):
        price = self.cleaned_data.get("price")
        if price < 0:
            raise forms.ValidationError("Цена не может быть отрицательной")
        return price


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ["name", "phone", "coach", "comment", "appointment_date", "schedules"]
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
            "appointment_date": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "schedules": forms.CheckboxSelectMultiple(
                attrs={"class": "form-check-input"}
            ),
        }

    def clean_appointment_date(self):
        appointment_date = self.cleaned_data.get("appointment_date")
        if appointment_date and appointment_date < timezone.now().date():
            raise forms.ValidationError("Дата записи не может быть в прошлом.")
        return appointment_date


    def clean_schedules(self):
        # Нам нужно добыть инструктора и все указанные практики из формы, добыть их из DB и проверить действительно ли инструктор назначил все эти практики

        schedules = self.cleaned_data.get("schedules")
        coach = self.cleaned_data.get("coach")

        if not coach or not schedules:
            raise forms.ValidationError("Вы должны выбрать инструктора и практики.")

        # Добывам все практики которые назначил этот инструктор на самом деле
        coach_schedules = coach.schedules.all()

        # Проверяем все ли практики которые выбрал пользователь назначил этот инструктор
        not_approved_schedules = []
        for schedule in schedules:
            if schedule not in coach_schedules:
                not_approved_schedules.append(schedule.name)

        if not_approved_schedules:
            raise forms.ValidationError("Этот инструктор не назначал следующие практики: " + ", ".join(not_approved_schedules))
        
        
        return schedules



