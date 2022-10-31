import django_filters
import ffmpeg as ffmpeg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import MultiPartParser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.transcribe.api.serializers import TranscribeSerializer, TranscribeDetailSerializer, CreateTranscribeSerializer
from apps.transcribe.exceptions import TranscribeNotFound
from apps.transcribe.models import Transcribe
from apps.transcribe.pagination import TranscribePagination
from apps.transcribe.tasks import save_transcribe_task
from apps.transcribe.utils import transcribe_ftp_path, clean_filename, delete_file, get_transcribe_price
from storage.ftp import FTPStorage


class TranscribeFilter(django_filters.FilterSet):
    lang = django_filters.CharFilter(field_name='lang', lookup_expr='iexact')
    status = django_filters.BooleanFilter(field_name='status', lookup_expr='iexact')
    duration = django_filters.NumberFilter()
    duration__gt = django_filters.NumberFilter(field_name="duration", lookup_expr="gt")
    duration__lt = django_filters.NumberFilter(field_name="duration", lookup_expr="lt")

    class Meta:
        model = Transcribe
        fields = ['lang', 'status', 'duration']


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
        transcribe_list = self.queryset.filter(user=user).order_by('-created')


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
    serializer_class = CreateTranscribeSerializer

    def post(self, request: Request):
        pass

#TODO
class TranscribeFileAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CreateTranscribeSerializer
    parser_classes = [MultiPartParser]

    def post(self, request: Request):
        user = request.user
        wallet = user.profile.wallet
        data = request.data
        audio_file = request.FILES.get('file')
        lang = data['lang']
        duration = float(ffmpeg.probe(audio_file.temporary_file_path())['format']['duration'])
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
        transcribe.save()
        data = {'transcribe_id': transcribe.id}
        save_transcribe_task.delay(data)
        # wallet.credit -= price
        # wallet.save()
        return Response("Transcribe saved", status=status.HTTP_201_CREATED)


@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def delete_transcribe_api_view(request: Request, transcribe_id):
    pass
