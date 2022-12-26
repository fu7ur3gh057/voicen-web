from django.urls import path
from .views import TranscribeFileAPIView, TranscribeListAPIView, TranscribeDetailAPIView, TranscribeYoutubeAPIView, \
    delete_transcribe_api_view, TranscribeAudioAPIView, delete_all_transcribes_api_view

urlpatterns = [
    path('', TranscribeListAPIView.as_view(), name='all'),
    path('detail/<str:transcribe_id>/', TranscribeDetailAPIView.as_view(), name='transcribe_detail'),
    path('audio/<str:transcribe_id>/', TranscribeAudioAPIView.as_view(), name='transcribe_stream'),
    path('upload/file/', TranscribeFileAPIView.as_view(), name='upload_file'),
    path('upload/youtube/', TranscribeYoutubeAPIView.as_view(), name='upload_youtube'),
    path('delete/', delete_transcribe_api_view, name='delete_transcribe'),
    path('delete/all/', delete_all_transcribes_api_view, name='delete_all_transcribes'),
]
