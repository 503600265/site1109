from django.urls import path, include, re_path
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.conf.urls import url

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('admin/', admin.site.urls),
    path('<int:labeling_id>/', views.detail, name='detail'),
    path('delete/<id>', views.delete, name='delete'),
    path('edit/<id>', views.edit, name='edit'),
    path('submit/', views.upload, name='submit'),
    path('Name/', views.NameView, name='Name'),
    path('Name/z-a/', views.NameViewZ_A, name='Name'),
    path('Publish/', views.PublishView, name='Publish'),
    path('Publish/mostrecent', views.PublishViewMostRecent, name='Publish')
]
