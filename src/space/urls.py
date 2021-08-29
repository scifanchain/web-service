from django.urls import path, include
from . import views

app_name = 'space'


urlpatterns = [
    path('', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('works/', views.works, name='works'),
    path('stage/<int:stage_id>/', views.get_stage, name='stage'),
    path('create_work/', views.create_work, name='create_work'),
    path('wallet/', views.wallet, name='wallet'),
    path('change_password/', views.change_password, name='change_password'),
    path('change_avatar/', views.change_avatar, name='change_avatar')
]
