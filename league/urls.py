from django.urls import path
from django.views.static import serve
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('leaguesignup/', views.leaguesignup, name='leaguesignup'),
    path('schedule/', views.schedule, name='schedule'),
    path('schedule/<int:league_id>/', views.schedule, name='schedule'),
    path('previousleagues/', views.previousleagues, name='previousleagues'),
    path('reportleaguescore/', views.reportLeagueScore, name='reportleaguescore'),
    path('updateleaguescore/', views.updateLeagueScore, name='updateleaguescore'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
