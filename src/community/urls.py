from django.urls import path

from . import views

app_name = 'community'

urlpatterns = [
    path('', views.home, name='home'),
    path('channel/<int:channel_id>/', views.channel, name='channel'),
    path('topic_list/<int:topic_id>/', views.topic_list, name='topic_list'),
    path('create_topic/', views.create_topic, name='create_topic'),
]
