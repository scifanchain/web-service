from django.urls import path
from . import views

app_name = 'works'

urlpatterns = [
    path('', views.index, name='index'),
    path('stage/<int:stage_id>/', views.stage_detail, name='stage_detail'),
    path('api/stage/list/', views.stage_list_json, name='stage_list_json'),
    path('api/stage/<int:pk>/', views.StageDetail.as_view(), name='api_stage'),
    path('stage/json/<int:stage_id>/', views.stage_json, name='stage_json'),
]
