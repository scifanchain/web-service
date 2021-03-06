from django.urls import path
from . import views

app_name = 'authors'


urlpatterns = [
    path('', views.home, name='home'),
    path('active_author_list/', views.ActiveAuthorList.as_view(),
         name='active_author_list'),
    path('profile/', views.profile, name='profile'),
    path('works/', views.works, name='works'),
    # stages
    path('stage/<int:stage_id>/', views.get_stage, name='stage'),
    path('create_stage/', views.create_stage, name='create_stage'),
    path('edit_stage/<int:stage_id>/', views.edit_stage, name='edit_stage'),
    # wallet
    path('wallet/', views.wallet, name='wallet'),
    path('save_wallet/', views.save_wallet, name='save_wallet'),
    path('wallets/<username>/', views.MyWallets.as_view(), name='wallets'),

    # avatar
    path('change_avatar/', views.ChangeAvatar.as_view(), name='change_avatar'),
    path('ex/', views.sign_ex, name='ex')
]
