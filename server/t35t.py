import os
from decimal import Decimal
import unicodedata
import string

from apps.transcribe.utils import get_transcribe_price, download_yt_video_as_mp3, get_youtube_video_info

# download_yt_video_as_mp3(video_url='https://www.youtube.com/watch?v=hS5CfP8n_js&ab_channel=Mr.Monk',
#                          user_id='d5f419d0-f4c1-4592-b7c6-9e22f8fabb78')

info = get_youtube_video_info('https://www.youtube.com/watch?v=hS5CfP8n_js&ab_channel=Mr.Monk')
path = download_yt_video_as_mp3(video_info=info, user_id='d5f419d0-f4c1-4592-b7c6-9e22f8fabb78')
file = open(path, 'rb')
print(file)
