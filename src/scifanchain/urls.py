from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from . import views
from django.conf.urls.static import static

from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets

from works.views import StageViewSet


# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register('users', UserViewSet)
router.register('stages', StageViewSet)

urlpatterns = [
    path('', views.home, name='home'),
    path('coming/', views.coming, name='coming'),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register/', views.register, name='register'),
    path('blogs/', include('blogs.urls'), name='blogs'),
    path('works/', include('works.urls'), name='works'),
    path('space/', include('space.urls'), name='space'),
    path('community/', include('community.urls'), name='community'),
    path('mdeditor/', include('mdeditor.urls')),
    path('summernote/', include('django_summernote.urls')),
    # api
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# 后台管理覆写
admin.site.site_title = settings.SITE_NAME
admin.site.site_header = settings.SITE_NAME
