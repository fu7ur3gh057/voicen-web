from django_countries.serializer_fields import CountryField
from rest_framework import serializers

from apps.profiles.models import Profile
from apps.synthesis.models import Synthesis


class SynthesisSerializer(serializers.ModelSerializer):
    language = serializers.CharField(source='lang')
    status = serializers.SerializerMethodField()

    def get_status(self, obj):
        if obj.status == -1:
            return "waiting"
        elif obj.status == 0:
            return "preparing"
        elif obj.status == 1:
            return "processing"
        elif obj.status == 2:
            return "synthesizing"
        elif obj.status == 3:
            return "ready"
        elif obj.status == 4:
            return "failed"
        else:
            return "unknown"

    class Meta:
        model = Synthesis
        fields = [
            'id',
            'filename',
            'text',
            '',
            'status',
            'created_at',
            '',
        ]


class CreateSynthesisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Synthesis
        fields = ['']
