from django import forms
from soccershop.models import Size

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]


class CartAddProductForm(forms.Form):
    """Создание формы для выбора количества товара и его размера"""
    sizes_all = Size.objects.all()
    choises = map(lambda s: (s.value, s.value), sizes_all)
    sizes = forms.ChoiceField(choices=choises)
    quantity = forms.TypedChoiceField(
        choices=PRODUCT_QUANTITY_CHOICES,
        coerce=int)
    update = forms.BooleanField(required=False,
                                initial=False,
                                widget=forms.HiddenInput)
