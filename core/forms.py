from django import forms
from .models import Coach, Practice, Application, Review
from django.utils import timezone
from datetime import datetime


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