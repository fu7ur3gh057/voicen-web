from django.urls import path

from .views import SynthesisListAPIView, SynthesisDetailAPIView, SynthesisTextAPIView, SynthesisFileAPIView, \
    delete_synthesis_api_view, SynthesisAudioAPIView

urlpatterns = [
    path('', SynthesisListAPIView.as_view(), name='all'),
    path('detail/<str:synthesis_id>/', SynthesisDetailAPIView.as_view(), name='synthesis_detail'),
    path('audio/<str:synthesis_id>/', SynthesisAudioAPIView.as_view(), name='synthesis_stream'),
    path('upload/text/', SynthesisTextAPIView.as_view(), name='upload_text'),
    path('upload/file/', SynthesisFileAPIView.as_view(), name='upload_file'),
    path('delete/<str:synthesis_id>/', delete_synthesis_api_view, name='delete_synthesis'),
]
