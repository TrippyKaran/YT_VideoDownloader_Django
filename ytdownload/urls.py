from django.urls import path
from . import views
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Add your existing URL patterns for download_audio and download_video here
    path("download_audio/", views.download_audio, name="download_audio"),
    # path("download_video/", views.download_video, name="download_video"),
    path("download_video/4K", views.download_video_4k, name="download_video_4k"),
    path("download_video/FHD", views.download_video_fhd, name="download_video_fhd"),
    path("download_video/HD", views.download_video_hd, name="download_video_hd"),
]
