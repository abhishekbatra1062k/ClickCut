from django.urls import path
from .views import home, redirect_url

urlpatterns = [
    path('', home, name='home'),
    path('<str:short_url>/', redirect_url, name='redirect'),
]