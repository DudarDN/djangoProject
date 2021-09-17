from django.urls import path, include
import soccershop
from soccershop import views
from . import views


urlpatterns = [
    path('', soccershop.views.product_list, name='product_list'),
    path('register/', views.register, name='register'),
    path('', include('django.contrib.auth.urls')),
    path('edit/', views.edit, name='edit'),
]
