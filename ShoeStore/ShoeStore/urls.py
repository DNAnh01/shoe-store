from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', views.HOME, name='home '),
    path('base/', views.BASE, name='base')
] + static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
