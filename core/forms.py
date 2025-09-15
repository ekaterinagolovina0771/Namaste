from django import forms
from .models import Application, Review, Schedule
from django.utils import timezone
from datetime import time


class ReviewModelForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["name", "text", "rating"]
        widgets = {
            "text": forms.Textarea(attrs={"placeholder": "Ваш отзыв", "class": "form-control"}),
            "name": forms.TextInput(attrs={"placeholder": "Ваше имя", "class": "form-control"}),
            "rating": forms.Select(attrs={"placeholder": "Ваша оценка", "class": "form-control"}),
        }

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ["name", "phone", "comment", "schedule"]
        widgets = {
            "name": forms.TextInput(
                attrs={"placeholder": "Ваше имя", "class": "form-control"}
            ),
            "phone": forms.TextInput(
                attrs={"placeholder": "+7 (999) 999-99-99", "class": "form-control"}
            ),
            "comment": forms.Textarea(
                attrs={
                    "placeholder": "Комментарий к заказу",
                    "class": "form-control",
                    "rows": 3,
                }
            ),
            "schedule": forms.Select(attrs={"class": "form-control"}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Добавьте расписание в список полей формы
        self.fields['schedule'].queryset = Schedule.objects.all()

class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ['date', 'start_time']
        widgets = {
            'date': forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            'start_time': forms.TimeInput(attrs={'type': 'time', 'step': '300'}),
        }