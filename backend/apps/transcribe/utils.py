from decimal import Decimal


def speechtotext_file_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'stt/user_{0}/{1}'.format(instance.profile.user.id, filename)


def get_filename(text):
    if len(text) > 40:
        return f'{text[:39]}'
    else:
        return f'{text}'


def get_filepath(filename, user_id):
    return f"media/stt/user_{user_id}/{filename}"


def get_stt_price(duration: float):
    stt_price = 0.06
    price = round((Decimal((duration) * int(stt_price) / 60)), 5)
    print('PRICE IS', price)
    return price
