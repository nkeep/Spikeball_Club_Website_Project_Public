from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Media
import urllib
import requests
import os

YOUTUBE_API_KEY = os.environ.get('YOUTUBE_API_KEY')
INSTAGRAM_API_KEY = os.environ.get('INSTAGRAM_API_KEY')

@receiver(post_save, sender=Media)
def getThumbnail(sender, instance, created, **kwargs):

    if created:
        if 'youtube' in str(instance.url):
            parsed_url = urllib.parse.urlparse(instance.url)
            video_id = urllib.parse.parse_qs(parsed_url.query).get('v')
            video_id = video_id[0]
            response = requests.get(f'https://youtube.googleapis.com/youtube/v3/videos?part=snippet&id={video_id}&key={YOUTUBE_API_KEY}')
            json = response.json()
            print(json)
            thumbnail = json['items'][0]['snippet']['thumbnails']['medium']['url']

            instance.thumbnail = thumbnail
            instance.save()

        if 'instagram' in str(instance.url):
            request = requests.get(f"https://graph.instagram.com/me/media?fields=id&access_token={INSTAGRAM_API_KEY}")
            print(request.text)
            media_id = request.json()['data'][instance.instagramIndex]['id']
            instance.media_id = media_id
            # urlrequest = requests.get(f"https://graph.instagram.com/{media_id}?fields=media_url&access_token={INSTAGRAM_API_KEY}")
            # media_url = urlrequest.json()["media_url"]
            # instance.thumbnail = media_url
            instance.save()
