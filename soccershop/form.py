from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):
    """Создание формы для отзыва о товаре"""
    class Meta:
        model = Review
        fields = ('name', 'email', 'body')
