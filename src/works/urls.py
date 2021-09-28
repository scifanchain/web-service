from django.urls import path
from . import views

app_name = 'works'

urlpatterns = [
    path('', views.index, name='index'),
    path('stage/update/<pk>/',views.StageDetail.as_view(), name='stage_update'),
    path('stage/delete/<pk>/',views.StageDetail.as_view(), name='stage_delete'),
    path('stage_list_by_author/', views.StageListByAuthor.as_view(), name='stage_list_by_author'),
    path('check_title', views.check_title, name='check_title'),
]

