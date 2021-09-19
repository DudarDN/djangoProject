from django.contrib import admin
from .models import Category, Product, SizeType, Size, Review


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Отображение модели Category на сайте администрирования."""
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(SizeType)
class SizeTypeAdmin(admin.ModelAdmin):
    """Отображение модели SizeType на сайте администрирования."""
    list_display = ['name']


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    """Отображение модели Size на сайте администрирования."""
    list_display = ['sizetype', 'value']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Отображение модели Product на сайте администрирования."""
    list_display = ['name', 'slug', 'price',
                    'available', 'created']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'available']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Отображение модели Review на сайте администрирования."""
    list_display = ('name', 'email', 'product', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')
