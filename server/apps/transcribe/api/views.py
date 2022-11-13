import json
import urllib.request
import isodate

import django_filters
import ffmpeg as ffmpeg
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import MultiPartParser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.transcribe.api.serializers import TranscribeSerializer, TranscribeDetailSerializer
from apps.transcribe.exceptions import TranscribeNotFound
from apps.transcribe.models import Transcribe
from apps.transcribe.pagination import TranscribePagination
from apps.transcribe.tasks import save_transcribe_file_task, save_transcribe_youtube_task, delete_transcribe_task
from apps.transcribe.utils import transcribe_ftp_path, clean_filename, delete_file, get_transcribe_price, youtube_id, \
    get_youtube_api_url, get_youtube_video_info
from storage.ftp import FTPStorage
from django.conf import settings


class TranscribeFilter(django_filters.FilterSet):
    lang = django_filters.CharFilter(field_name='lang', lookup_expr='iexact')
    status = django_filters.BooleanFilter(field_name='status', lookup_expr='iexact')
    duration = django_filters.NumberFilter()
    duration__gt = django_filters.NumberFilter(field_name="duration", lookup_expr="gt")
    duration__lt = django_filters.NumberFilter(field_name="duration", lookup_expr="lt")

    class Meta:
        model = Transcribe
        fields = ['lang', 'status', 'duration']


# GET ALL TRANSCRIBE JOBS
class TranscribeListAPIView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TranscribeSerializer
    queryset = Transcribe.objects.all()
    pagination_class = TranscribePagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = TranscribeFilter
    search_fields = ['lang', 'status']

    def get_queryset(self):
        user = self.request.user
        transcribe_list = self.queryset.filter(profile=user.profile).order_by('-created_at')
        return transcribe_list


# GET TRANSCRIBE BY ID
class TranscribeDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TranscribeDetailSerializer

    def get(self, request: Request, transcribe_id):
        try:
            transcribe_job = Transcribe.objects.get(id=transcribe_id)
        except Transcribe.DoesNotExist:
            raise TranscribeNotFound
        serializer = self.serializer_class(transcribe_job, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class TranscribeYoutubeAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TranscribeSerializer

    def post(self, request: Request):
        try:
            user = request.user
            wallet = user.profile.wallet
            data = request.data
            youtube_url = data['youtube_url']
            lang = data['lang']
            # Get Youtube video info
            video_info = get_youtube_video_info(youtube_url)
            duration = float(video_info['duration'])
            video_title = video_info['title']
            # Video is too short
            if int(duration) < 1:
                return Response('Be sure your url is correct', status=status.HTTP_400_BAD_REQUEST)
            # Get price
            price = get_transcribe_price(duration=duration)
            # if price > wallet.credit:
            #     err_msg = 'You have not enough balance.'
            #     return Response(err_msg, status=status.HTTP_402_PAYMENT_REQUIRED)
            file_name = f'{video_title}.mp3'
            transcribe = Transcribe.objects.create(
                profile=user.profile,
                file_name=file_name,
                youtube_url=youtube_url,
                lang=lang,
                duration=duration,
                price=price
            )
            transcribe.save()
            # Celery Task
            data = {'transcribe_id': transcribe.id, 'video_info': video_info}
            save_transcribe_youtube_task.delay(data)
            # Change Wallet
            wallet.credit -= price
            wallet.save()
            serializer = self.serializer_class(transcribe)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception:
            return Response('Be sure your url is correct', status=status.HTTP_400_BAD_REQUEST)


# UPLOAD TRANSCRIBE BY FILE
class TranscribeFileAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser]
    serializer_class = TranscribeSerializer

    def post(self, request: Request):
        user = request.user
        wallet = user.profile.wallet
        data = request.data
        audio_file = request.FILES.get('file')
        lang = data['lang']
        # Get duration
        duration = float(ffmpeg.probe(audio_file.temporary_file_path())['format']['duration'])
        # Get price
        price = get_transcribe_price(duration=duration)
        if price > wallet.credit:
            err_msg = 'You have not enough balance.'
            return Response(err_msg, status=status.HTTP_402_PAYMENT_REQUIRED)
        file_name = audio_file.name
        transcribe = Transcribe.objects.create(
            profile=user.profile,
            file=audio_file,
            file_name=file_name,
            lang=lang,
            duration=duration,
            price=price
        )
        print(f'{type(transcribe.file)}')
        transcribe.save()
        # Celery Task
        data = {'transcribe_id': transcribe.id}
        save_transcribe_file_task.delay(data)
        # Change Wallet
        wallet.credit -= price
        wallet.save()
        serializer = self.serializer_class(transcribe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# DELETE TRANSCRIBE BY ID
@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def delete_transcribe_api_view(request: Request, transcribe_id):
    transcribe = get_object_or_404(Transcribe, id=transcribe_id)
    if transcribe is None:
        err_msg = 'Job is not found'
        return Response(err_msg, status=status.HTTP_404_NOT_FOUND)
    # Celery Task
    data = {'ftp_path': transcribe.ftp_path}
    delete_transcribe_task.delay(data)
    transcribe.delete()
    return Response('Transcribe job was deleted successfuly', status=status.HTTP_200_OK)
