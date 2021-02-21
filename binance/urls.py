from django.urls import path
from . import views
from binance.views import KeyFormView, HomeView

app_name = 'binance'
urlpatterns = [
    path('keys/', KeyFormView.as_view()),
    path('home/', HomeView.as_view()),
    #path('', HomeView.as_view(), name='home'),
]
