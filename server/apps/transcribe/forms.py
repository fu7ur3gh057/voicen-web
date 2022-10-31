from django import forms
from django.utils.translation import gettext_lazy as _

from apps.transcribe.models import Transcribe


class TranscribeForm(forms.ModelForm):
    class Meta:
        model = Transcribe
        fields = ['file']
        widgets = {
            'file': forms.FileInput(attrs={'accept': 'audio/*,video/*', 'multiple': True}),
        }