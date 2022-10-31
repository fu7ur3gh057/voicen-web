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


def synthesis_ftp_path():
    pass
