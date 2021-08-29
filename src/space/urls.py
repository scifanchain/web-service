from django.urls import path, include
from . import views

app_name = 'space'


urlpatterns = [
    path('', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('works/', views.works, name='works'),
    # stages
    path('stage/<int:stage_id>/', views.get_stage, name='stage'),
    path('create_stage/', views.create_stage, name='create_stage'),
    path('edit_stage/<int:stage_id>/', views.edit_stage, name='edit_stage'),
    # wallet
    path('wallet/', views.wallet, name='wallet'),
    # password
    path('change_password/', views.change_password, name='change_password'),
    path('change_avatar/', views.change_avatar, name='change_avatar')
]
