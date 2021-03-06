from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from soccershop.models import Product
from .cart import Cart
from .forms import CartAddProductForm


@require_POST
def cart_add(request, product_id):
    """Обработчик для добавления товаров в корзину."""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 size=cd['sizes'],
                 )
    return redirect('cart:cart_detail')


def cart_remove(request, product_id, size):
    """Обработчик удаления товара из корзины"""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product, size)
    return redirect('cart:cart_detail')


def cart_detail(request):
    """Обработчик для страницы списка товаров, добавленных вкорзину."""
    cart = Cart(request)

    return render(request, 'cart/details.html', {'cart': cart})
