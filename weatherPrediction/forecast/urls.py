from django.urls import path
from . import views


urlpatterns = [
    path('', views.index_view, name='home'),              # Home page
    path('weather/', views.weather_view, name='weather'), # Weather forecast
    path('about/', views.about_view, name='about'),
]