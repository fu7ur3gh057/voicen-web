from django.urls import path
from .views import TranscribeFileAPIView, TranscribeListAPIView, TranscribeDetailAPIView, delete_transcribe_api_view

urlpatterns = [
    path('', TranscribeListAPIView.as_view(), name='all'),
    path('detail/<str:transcribe_id>/', TranscribeDetailAPIView.as_view(), name='transcribe_detail'),
    path('upload/file/', TranscribeFileAPIView.as_view(), name='upload_file'),
    path('delete/<str:transcribe_id>/', delete_transcribe_api_view, name='delete_file'),
]
