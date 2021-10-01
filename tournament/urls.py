from django.urls import path
from . import views

urlpatterns = [
    path('', views.tournament, name='tournament'),
    path('tournamentbracket/', views.tournamentbracket, name='tournamentbracket'),
    path('tournamentbracket/<int:tournament_id>/', views.tournamentbracket, name='tournamentbracket'),
    path('tournamentpayments/<int:tournament_id>/', views.tournamentpayments, name='tournamentpayments'),
    path('previoustournaments/', views.previoustournaments, name='previoustournaments'),
    path('tournamentsignup/', views.tournamentsignup, name='tournamentsignup'),
    path('addteam/', views.addteam, name='addteam'),
]
