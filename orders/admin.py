from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    """Добавление модели OrderItem в виде списка связанных объектов."""
    model = OrderItem
    raw_id_fields = ['product']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Отображение модели Order на сайте администрирования."""
    list_display = ['id', 'first_name', 'last_name', 'phone', 'email',
                    'address', 'postal_code', 'city', 'paid',
                    'created']
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]
