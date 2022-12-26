from os.path import splitext
from urllib.parse import urlparse

import django_filters
import magic
import textract
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import MultiPartParser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.synthesis.api.serializers import SynthesisSerializer, SynthesisDetailSerializer
from apps.synthesis.exceptions import SynthesisNotFound
from apps.synthesis.models import Synthesis
from apps.synthesis.pagination import SynthesisPagination
from apps.synthesis.utils import remove_text_inside_brackets, get_synthesis_price, get_short_text, get_lang_for_textract
from constants.voicen_constants import AVAILABLE_SYNTHESIS_LANGS, AVAILABLE_VOICE_IDS
from storage.ftp import FTPStorage
from apps.synthesis.tasks import delete_synthesis_task


class SynthesisFilter(django_filters.FilterSet):
    lang = django_filters.CharFilter(field_name='lang', lookup_expr='iexact')
    status = django_filters.BooleanFilter(field_name='status', lookup_expr='iexact')
    char_count = django_filters.NumberFilter()
    char_count__gt = django_filters.NumberFilter(field_name="char_count", lookup_expr="gt")
    char_count__lt = django_filters.NumberFilter(field_name="char_count", lookup_expr="lt")

    class Meta:
        model = Synthesis
        fields = ['lang', 'status', 'char_count']


# GET ALL SYNTHESIS JOBS
class SynthesisListAPIView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SynthesisSerializer
    queryset = Synthesis.objects.all()
    pagination_class = SynthesisPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = SynthesisFilter
    search_fields = ['lang', 'status']

    def get_queryset(self):
        user = self.request.user
        synthesis_list = self.queryset.filter(profile=user.profile).order_by('-created_at')
        return synthesis_list


# GET SYNTHESIS BY ID
class SynthesisDetailAPIView(APIView):
    serializer_class = SynthesisDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request, synthesis_id):
        try:
            synthesis_job = Synthesis.objects.get(id=synthesis_id)
        except Synthesis.DoesNotExist:
            raise SynthesisNotFound
        serializer = self.serializer_class(synthesis_job, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)


# GET SYNTHESIS FILE STREAM BYTES
class SynthesisAudioAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request, synthesis_id):
        try:
            # Get Synthesis Job
            synthesis_job = Synthesis.objects.get(id=synthesis_id)
            ftp_storage = FTPStorage()
            # Get Correct FTP Path
            ftp_path = urlparse(synthesis_job.ftp_path).path
            # Get FTP File
            ftp_file = ftp_storage._open(name=ftp_path, mode='rb')
            # Get Mime Type
            mime_type = magic.from_buffer(buffer=ftp_file.read(1024), mime=True)
            ftp_file.seek(0)
            response = HttpResponse()
            response.write(content=ftp_file.read())
            response['Content-Type'] = mime_type
            response['Accept-Ranges'] = 'bytes'
            response['Content-Disposition'] = f'attachment; filename={synthesis_job.file_name}{splitext(ftp_path)[1]}'
            response['Content-Length'] = ftp_storage.file_size(ftp_path)
            return response
        except Synthesis.DoesNotExist:
            raise SynthesisNotFound
        except Exception as ex:
            return Response(f'{ex}', status=status.HTTP_400_BAD_REQUEST)


# UPLOAD SYNTHESIS BY FILE
class SynthesisTextAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SynthesisDetailSerializer

    def post(self, request: Request):
        user = request.user
        wallet = user.profile.wallet
        data = request.data
        lang = data['lang']
        text = data['text'].strip()
        voice_id = data['voice_id']
        text_len = remove_text_inside_brackets(text=text)
        err_msg = None
        if lang not in AVAILABLE_SYNTHESIS_LANGS:
            err_msg = 'Incorrect language'
        elif voice_id not in AVAILABLE_VOICE_IDS:
            err_msg = 'Incorrect voice_id'
        elif text_len < 3:
            err_msg = 'Your text must have at least 3 or more characters length'
        if err_msg is not None:
            return Response(f'Error: {err_msg}', status=status.HTTP_400_BAD_REQUEST)
        price = get_synthesis_price(char_size=text_len)
        if price > wallet.credit:
            err_msg = 'You have not enough balance.'
            return Response(err_msg, status=status.HTTP_402_PAYMENT_REQUIRED)
        file_name = get_short_text(text=text)
        synthesis = Synthesis.objects.create(
            profile=user.profile,
            text=text,
            file_name=file_name,
            lang=lang,
            char_count=text_len,
            price=price,
            voice_id=voice_id
        )
        synthesis.save()
        wallet.credit -= price
        wallet.save()
        serializer = self.serializer_class(synthesis)
        return Response(serializer.data, status=status.HTTP_200_OK)


# UPLOAD SYNTHESIS BY FILE
class SynthesisFileAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser]
    serializer_class = SynthesisSerializer

    def post(self, request: Request):
        user = request.user
        wallet = user.profile.wallet
        data = request.data
        file = request.FILES.get('file')
        voice_id = data['voice_id']
        # get specific lang for textract
        textract_lang = get_lang_for_textract(data=data)
        lang = data['lang']
        # read text from file
        text = textract.process(file.temporary_file_path(),
                                method='tesseract',
                                language=textract_lang).decode("utf-8")
        text = text.strip()
        text_len = remove_text_inside_brackets(text=text)
        err_msg = None
        if lang not in AVAILABLE_SYNTHESIS_LANGS:
            err_msg = 'Incorrect language'
        elif voice_id not in AVAILABLE_VOICE_IDS:
            err_msg = 'Incorrect voice_id'
        elif text_len < 3:
            err_msg = 'Your text must have at least 3 or more characters length'
        if err_msg is not None:
            return Response(f'Error: {err_msg}', status=status.HTTP_400_BAD_REQUEST)
        price = get_synthesis_price(char_size=text_len)
        if price > wallet.credit:
            err_msg = 'You have not enough balance.'
            return Response(err_msg, status=status.HTTP_402_PAYMENT_REQUIRED)
        file_name = get_short_text(text=text)
        synthesis = Synthesis.objects.create(
            profile=user.profile,
            text=text,
            file_name=file_name,
            lang=lang,
            char_count=text_len,
            price=price,
            voice_id=voice_id
        )
        synthesis.save()
        wallet.credit -= price
        wallet.save()
        serializer = self.serializer_class(synthesis)
        return Response(serializer.data, status=status.HTTP_200_OK)


# DELETE SYNTHESIS BY ARRAY OF IDs
@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def delete_synthesis_api_view(request: Request):
    job_id_list = request.data['job_id_list']
    data = {'id_list': job_id_list}
    delete_synthesis_task.delay(data)
    return Response('Transcribe jobs was deleted successfuly', status=status.HTTP_200_OK)
