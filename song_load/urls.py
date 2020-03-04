from django.urls import path

from . import views

urlpatterns = [
    path('upload', views.upload, name='song uploading'),
    path('download', views.download, name='get song vocal by song\'s hash')
]
