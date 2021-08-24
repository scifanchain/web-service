from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from . import views
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register/', views.register, name='register'),
    path('blogs/', include('blogs.urls'), name='blogs'),
    path('works/', include('works.urls'), name='works'),
    path('space/', include('space.urls'), name='space'),
    path('mdeditor/', include('mdeditor.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# 后台管理覆写
admin.site.site_title = settings.SITE_NAME
admin.site.site_header = settings.SITE_NAME
