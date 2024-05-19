from django.urls import path
from . import views
from binance.views import KeyFormView, HomeView, BuyOrderView, SellOrderView, CancelOrderView, TradeHistoryView

app_name = 'binance'
urlpatterns = [
    path('keys/', KeyFormView.as_view()),
    path('home/', HomeView.as_view()),
    path('buy/', BuyOrderView.as_view()),
    path('sell/', SellOrderView.as_view()),
    path('cancel/', CancelOrderView.as_view()),
    path('trade-history/', TradeHistoryView.as_view()),
]
