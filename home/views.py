from django.shortcuts import render
from .models import Media, Org, Photo
import os
import requests

INSTAGRAM_API_KEY = os.environ.get('INSTAGRAM_API_KEY')

def home(request):
    #refresh the API key when someone comes to the home page (it gets reset every 60 days, maybe there's a better way to do it?)
    requests.get(f"https://graph.instagram.com/refresh_access_token?grant_type=ig_refresh_token&access_token={INSTAGRAM_API_KEY}")
    gallery = Photo.objects.all()
    return render(request, 'home/home.html', {'gallery':gallery})

def media(request):
    medias = Media.objects.order_by("-date")

    for i in range(len(medias)):
        if "instagram" in medias[i].url:
            urlrequest = requests.get(f"https://graph.instagram.com/{medias[i].media_id}?fields=media_url&access_token={INSTAGRAM_API_KEY}")
            media_url = urlrequest.json()["media_url"]
            medias[i].thumbnail = media_url
            medias[i].save()

    return render(request,'home/media.html', {'medias':medias})

def community(request):
    orgs = Org.objects.all()
    return render(request, 'home/community.html', {'orgs':orgs})

def aboutus(request):

    return render(request, 'home/aboutus.html')

def releasewaiver(request):

    return render(request, 'home/releasewaiver.html')
