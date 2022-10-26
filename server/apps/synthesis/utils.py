import re
from decimal import Decimal


def remove_text_inside_brackets(text):
    result = re.sub("[\{\(\[].*?[\)\}\]]", "", text, flags=re.S)
    return len(result)


def get_synthesis_price(char_size: int):
    tts_price = 0.05
    price = round((Decimal((char_size * tts_price) / 1000)), 5)
    print('PRICE IS', price)
    return price




def get_filename(text):
    if len(text) > 40:
        return f'{text[:39]}'
    else:
        return f'{text}'


def get_filepath(filename, user_pkid):
    return f"media/tts/user_{user_pkid}/{filename}.wav"
