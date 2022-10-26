from django.utils.translation import gettext_lazy as _

START_CREDIT = 1.20  # dollar

AVALIABLE_VOICE_IDS = ['325640', '325641', '325642',
                       '325643', '325644', '325645',
                       '325646', '325647', '325648']

VOICE_CHOICES = (
    (325640, 'Aytac, AZ, female'),
    (325641, 'Aynur, AZ, female'),
    (325642, 'Ramin, AZ, male'),
    (325643, 'Elchin, AZ, male'),
    (325648, 'Kamil, AZ, male'),
    (325647, 'Zeynep, TR, female'),
    (325646, 'Mesut, TR, male'),
    (325644, 'Sibel, TR, female'),
    (325645, 'Anna, RU, female'),
)

VOICE_TUPLE = (
    (325640, 'az', 'Aytac', _('female')),
    (325641, 'az', 'Aynur', _('female')),
    (325642, 'az', 'Ramin', _('male')),
    # (325643, 'az', 'Elchin', _('male')),
    (325648, 'az', 'Kamil', _('male')),
    (325647, 'tr', 'Zeynep', _('female')),
    (325646, 'tr', 'Mesut', _('male')),
    (325644, 'tr', 'Sibel', _('female')),
    (325645, 'ru', 'Anna', _('female')),
)

VOICE_LANG_VOICE_DICT = {
    'az': ['Aytac', 'Aynur', 'Ramin', 'Kamil'],
    'tr': ['Zeynep', 'Mesut', 'Sibel'],
    'ru': ['Anna']
}

VOICE_DICT = {
    325640: 'Aytac',
    325641: 'Aynur',
    325642: 'Ramin',
    325643: 'Elchin',
    325648: 'Kamil',
    325647: 'Zeynep',
    325646: 'Mesut',
    325644: 'Sibel',
    325645: 'Anna',
}

VOICE_DICT_REVERSE = {
    'Aytac': 325640,
    'Aynur': 325641,
    'Ramin': 325642,
    'Elchin': 325643,
    'Kamil': 325648,
    'Zeynep': 325647,
    'Mesut': 325646,
    'Sibel': 325644,
    'Anna': 325645
}

VOICE_PITCH_TEMPO = {
    325640: {'pitch': 0.5, 'tempo': 1},  # Aytac
    325641: {'pitch': 0.5, 'tempo': 1},  # Aynur
    325642: {'pitch': 0.5, 'tempo': 1},  # Ramin
    325643: {'pitch': 0.5, 'tempo': 1},  # Elchin
    325648: {'pitch': 0.5, 'tempo': 1},  # Kamil
    325647: {'pitch': 0.5, 'tempo': 1},  # Zeynep
    325646: {'pitch': 0.5, 'tempo': 1},  # Mesut
    325644: {'pitch': 0.5, 'tempo': 1},  # Sibel
    325645: {'pitch': 0.5, 'tempo': 1},  # Anna'
}

allowed_extensions = ['mp3', 'midi', 'mid', 'cda', 'aif', 'ogg', 'wav', 'mpa', 'wpl', 'opus',
                       '3g2', '3gp', 'avi', 'flv', 'h264', 'm4v', 'm4a', 'mkv', 'mov', 'mp4',
                       'mpg', 'mpeg', 'mpeg4', 'amr', 'rm', 'swf', 'vob', 'wmv', 'webm', 'aac']
