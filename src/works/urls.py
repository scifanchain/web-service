from django.urls import path
from . import views

app_name = 'works'

urlpatterns = [
    path('', views.index, name='index'),
    path('check_title', views.check_title, name='check_title'),
]

