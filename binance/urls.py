from django.urls import path
from . import views
from binance.views import KeyFormView

app_name = 'binance'
urlpatterns = [
    #path('keys/', views.keyform_view),
    path('keys/', KeyFormView.as_view()),
    #path('login/', views.login),
    #path('index/', views.index)
]
