from django.urls import path, include
from . import views


app_name = 'space'

urlpatterns = [
    path('', views.home, name='home'),
    path('change_avatar', views.change_avatar, name='change_avatar')
]