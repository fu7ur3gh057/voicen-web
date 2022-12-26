from django_countries.serializer_fields import CountryField
from rest_framework import serializers

from apps.profiles.models import Profile
from apps.synthesis.models import Synthesis
from apps.synthesis.utils import get_synthesis_status


class SynthesisSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    short_text = serializers.SerializerMethodField()

    def get_short_text(self, obj):
        return obj.text[0:80]

    def get_status(self, obj):
        return get_synthesis_status(status=obj.status)

    class Meta:
        model = Synthesis
        fields = [
            'id',
            'file_name',
            'short_text',
            'voice_id',
            'lang',
            'char_count',
            'status',
            'created_at',
        ]


class SynthesisDetailSerializer(serializers.ModelSerializer):
    language = serializers.CharField(source='lang')
    status = serializers.SerializerMethodField()

    def get_status(self, obj):
        return get_synthesis_status(status=obj.status)

    class Meta:
        model = Synthesis
        fields = [
            'id',
            'file_name',
            'ftp_path',
            'text',
            'voice_id',
            'language',
            'char_count',
            'status',
            'created_at',
            'price'
        ]
