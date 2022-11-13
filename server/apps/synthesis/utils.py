import re
from decimal import Decimal

allowed_extensions = ['mp3', 'midi', 'mid', 'cda', 'aif', 'ogg', 'wav', 'mpa', 'wpl', 'opus',
                      '3g2', '3gp', 'avi', 'flv', 'h264', 'm4v', 'm4a', 'mkv', 'mov', 'mp4',
                      'mpg', 'mpeg', 'mpeg4', 'amr', 'rm', 'swf', 'vob', 'wmv', 'webm', 'aac']


def remove_text_inside_brackets(text):
    result = re.sub("[\{\(\[].*?[\)\}\]]", "", text, flags=re.S)
    return len(result)


def get_synthesis_price(char_size: int):
    tts_price = 0.05
    price = round((Decimal((char_size * tts_price) / 1000)), 5)
    print('PRICE IS', price)
    return price


def get_short_text(text: str):
    if len(text) > 50:
        return text[:50] + '...'
    else:
        return text[:50]


def synthesis_ftp_path():
    pass


def get_lang_for_textract(data):
    if data['lang'] == 'az':
        lang = 'aze'
    elif data['lang'] == 'ru':
        lang = 'rus'
    elif data['lang'] == 'tr':
        lang = 'tur'
    else:
        lang = 'eng'
    return lang


# GET TRANSCRIBE STATUS
def get_synthesis_status(status: int):
    if status == -1:
        return "waiting"
    elif status == 0:
        return "preparing"
    elif status == 1:
        return "processing"
    elif status == 2:
        return "synthesizing"
    elif status == 3:
        return "ready"
    elif status == 4:
        return "failed"
    else:
        return "unknown"
