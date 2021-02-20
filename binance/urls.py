from django.urls import path
from . import views

app_name = 'binance'
urlpatterns = [
    path('login/', views.login),
    path('index/', views.index)
]
