import os
from decimal import Decimal
import unicodedata
import string

valid_filename_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
char_limit = 250


def clean_filename(filename, whitelist=valid_filename_chars, replace=' '):
    # replace spaces
    filename, extension = os.path.splitext(filename)
    for r in replace:
        filename = filename.replace(r, '_')
    # keep only valid ascii chars
    cleaned_filename = unicodedata.normalize(
        'NFKD', filename).encode('ASCII', 'ignore').decode()
    # keep only whitelisted chars
    cleaned_filename = ''.join(c for c in cleaned_filename if c in whitelist)
    return cleaned_filename[:char_limit] + extension


file_name = 'salam_fuad necəsen.mp3'
print(clean_filename(filename=file_name))