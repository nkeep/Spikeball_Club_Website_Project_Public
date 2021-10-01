from django.db import models
from phone_field import PhoneField
from django.contrib.auth.models import User

class PaymentOption(models.Model):
    option = models.TextField(null=True, blank=True, max_length=100)

    def __str__(self):
        return self.option

class TTeam(models.Model): #Tournament Team
    team_name = models.CharField(max_length=30)
    teammate1 = models.CharField(max_length=15, default="Teammate1")
    teammate2 = models.CharField(max_length=15, default="Teammate2")
    teammate1_phone = PhoneField(blank=True, help_text='Contact phone number', default="56709")
    teammate2_phone = PhoneField(blank=True, help_text='Contact phone number', default="56709")
    seed = models.IntegerField(blank=True, default="0")
    payment = models.ForeignKey(PaymentOption, blank=True, null=True, on_delete=models.SET_NULL)
    paid = models.BooleanField(null=True, blank=True)
    #Stuff for pools
    team_number = models.IntegerField(blank=True, null=True) #Used for generating pools matches
    points_for = models.IntegerField(default=0)
    points_against = models.IntegerField(default=0)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    point_differential = models.IntegerField(default=0)

    class Meta:
        ordering = ['losses', '-point_differential']

    def __str__(self):
        return str(self.team_name)

class TMatch(models.Model): #Tournament Match
    team1 = models.ForeignKey(TTeam, on_delete = models.SET_NULL, related_name="Team1", blank=True, null=True)
    team2 = models.ForeignKey(TTeam, on_delete = models.SET_NULL, related_name="Team2", blank=True, null=True)
    winner = models.BooleanField(default=False)
    team1_score = models.IntegerField(blank=True, null=True)
    team2_score = models.IntegerField(blank=True, null=True)
    match_number= models.IntegerField(blank=True, null=True)
    parent_match = models.IntegerField(blank=True, null=True)
    parent_game = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return (str(self.team1) + " vs " + str(self.team2))



class PMatch(models.Model): #Pools match
    team1 = models.ForeignKey(TTeam, on_delete = models.SET_NULL, related_name="PTeam1", blank=True, null=True)
    team2 = models.ForeignKey(TTeam, on_delete = models.SET_NULL, related_name="PTeam2", blank=True, null=True)
    winner = models.BooleanField(default=False)
    team1_score = models.IntegerField(blank=True, null=True)
    team2_score = models.IntegerField(blank=True, null=True)
    match_number= models.IntegerField(blank=True, null=True)

    def __str__(self):
        return (str(self.team1) + " vs " + str(self.team2))

class PRound(models.Model):
    matches=models.ManyToManyField(PMatch, blank=True)
    round_number = models.IntegerField(blank=True, null=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return("Round " + str(self.round_number))

class Pool(models.Model): #Stores matches for each pool
    teams = models.ManyToManyField(TTeam, blank=True)
    rounds = models.ManyToManyField(PRound, blank=True)
    poolNumber = models.IntegerField(blank=True, null=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.poolNumber)



# Create your models here.
class Tournament(models.Model):
    name = models.CharField(max_length=50, default = "Tournament")
    date = models.DateTimeField()
    location = models.CharField(max_length=50)
    poster = models.ImageField(blank=True, null=True)
    teams = models.ManyToManyField(TTeam, blank=True)
    matches = models.ManyToManyField(TMatch, blank=True)
    pools = models.ManyToManyField(Pool, blank=True)
    pools_completed = models.BooleanField(default=False)
    password = models.CharField(max_length=20, blank=True, null=True)
    payment_options = models.ManyToManyField(PaymentOption, blank=True)
    entry_price = models.IntegerField(blank=True, null=True)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.name)
