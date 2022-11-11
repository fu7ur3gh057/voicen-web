from rest_framework import serializers

from apps.transcribe.models import Transcribe
from apps.transcribe.utils import get_transcribe_status


class TranscribeSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    def get_status(self, obj):
        return get_transcribe_status(status=obj.status)

    class Meta:
        model = Transcribe
        fields = [
            'id',
            'file_name',
            'youtube_url',
            'full_text',
            'duration',
            'price',
            'lang',
            'status',
            'created_at',
        ]


class TranscribeDetailSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    def get_status(self, obj):
        return get_transcribe_status(status=obj.status)

    class Meta:
        model = Transcribe
        # exclude = ['profile']
        fields = [
            'id',
            'file_name',
            'ftp_path',
            'youtube_url',
            'full_text',
            'edited_json',
            'duration',
            'price',
            'lang',
            'status',
            'created_at',
        ]


class CreateTranscribeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transcribe
        exclude = ['pkid']