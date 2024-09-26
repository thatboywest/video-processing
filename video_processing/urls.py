from django.urls import path
from . import views

app_name = 'video_processing'

urlpatterns = [
    path('', views.upload_video, name='upload_video'),
 
]