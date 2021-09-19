from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Отображение модели Profile на сайте администрирования."""
    list_display = ['user',
                    'phone',
                    'city',
                    'address',
                    'postal_code',
                    'date_of_birth',
                    'photo']
