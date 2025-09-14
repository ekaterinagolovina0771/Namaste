from django import forms
from .models import Coach, Practice, Application, Review, Schedule
from django.utils import timezone
from datetime import time


class ReviewModelForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["name", "text", "rating", "photo"]
        widgets = {
            "text": forms.Textarea(attrs={"class": "form-control"}),
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "rating": forms.Select(attrs={"class": "form-control"}),
            "photo": forms.FileInput(attrs={"class": "form-control"}),
        }

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ["name", "phone", "comment", "appointment_date", "appointment_time"]
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
            "appointment_date": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "appointment_time": forms.TimeInput(
                attrs={"type": "time", "class": "form-control"}
            ),
        }

class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ['date', 'start_time', 'location']
        widgets = {
            'date': forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            'start_time': forms.TimeInput(attrs={'type': 'time', 'step': '300'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
        }