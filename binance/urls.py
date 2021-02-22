from django.urls import path
from . import views
from binance.views import KeyFormView, HomeView, BuyOrderView, SellOrderView

app_name = 'binance'
urlpatterns = [
    path('keys/', KeyFormView.as_view()),
    path('home/', HomeView.as_view()),
    path('buy/', BuyOrderView.as_view()),
    path('sell/', SellOrderView.as_view()),
]
