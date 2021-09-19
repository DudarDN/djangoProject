from django import forms
from .models import Order


class OrderCreateForm(forms.ModelForm):
    """Класс для представления формы заказа"""
    class Meta:
        model = Order
        fields = ['first_name',
                  'last_name',
                  'phone',
                  'email',
                  'city',
                  'address',
                  'postal_code']
