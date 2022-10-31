from django.urls import path
from .views import TranscribeFileAPIView

urlpatterns = [
    path('upload/file/', TranscribeFileAPIView.as_view(), name='upload_file'),
]
