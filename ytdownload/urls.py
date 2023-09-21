from django.urls import path
from . import views

urlpatterns = [
    # Add your existing URL patterns for download_audio and download_video here
    path('download_audio/', views.download_audio, name='download_audio'),
    path('download_video/', views.download_video, name='download_video'),
]