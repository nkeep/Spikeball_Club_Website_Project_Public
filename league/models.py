from django.db import models
from phone_field import PhoneField
from django.contrib.auth.models import User

# Create your models here.

class Team(models.Model):
    team_name = models.CharField(max_length=30)
    teammate1 = models.CharField(max_length=15)
    teammate2 = models.CharField(max_length=15)
    teammate1_phone = PhoneField(blank=True, help_text='Contact phone number')
    teammate2_phone = PhoneField(blank=True, help_text='Contact phone number')

    points_for = models.IntegerField(default=0)
    points_against = models.IntegerField(default=0)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    point_differential = models.IntegerField(default=0)
    seed = models.IntegerField(default=0)

    class Meta:
        ordering = ['losses', '-point_differential']

    def __str__(self):
        return (self.team_name)

class Match(models.Model):
    team1 = models.ForeignKey(Team, on_delete = models.CASCADE, related_name="Team1", blank=True, null=True)
    team2 = models.ForeignKey(Team, on_delete = models.CASCADE, related_name="Team2", blank=True, null=True)
    winner1 = models.BooleanField(default=False)
    winner2 = models.BooleanField(default=False)
    winner3 = models.BooleanField(default=False)
    game1_team1_score = models.IntegerField(blank=True, null=True)
    game1_team2_score = models.IntegerField(blank=True, null=True)
    game2_team1_score = models.IntegerField(blank=True, null=True)
    game2_team2_score = models.IntegerField(blank=True, null=True)
    game3_team1_score = models.IntegerField(blank=True, null=True)
    game3_team2_score = models.IntegerField(blank=True, null=True)
    week_number = models.IntegerField(blank=True, null=True)
    round_number = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return ("Week: " + str(self.week_number) + " " + "Round: " + str(self.round_number) + " " + self.team1.team_name + " vs " + self.team2.team_name)

class TMatch(models.Model):
    team1 = models.ForeignKey(Team, on_delete = models.CASCADE, related_name="TTeam1", blank=True, null=True)
    team2 = models.ForeignKey(Team, on_delete = models.CASCADE, related_name="TTeam2", blank=True, null=True)
    team1_score = models.IntegerField(blank=True, null=True)
    team2_score = models.IntegerField(blank=True, null=True)
    match_number= models.IntegerField(blank=True, null=True)
    round_number = models.IntegerField(blank=True, null=True)
    winner = models.BooleanField(default=False)

    def __str__(self):
        return ("Round: " + str(self.round_number) + " Match: " + str(self.match_number) + str(self.team1) + " vs " + str(self.team2))

class Bracket(models.Model):
    bracket_num = models.IntegerField(blank=True, null=True)
    sub_bracket_num = models.IntegerField(blank=True, null=True) #Keeps track of consolation brackets, main =1, for 3rd = 2, 5-8 = 3 etc
    matches = models.ManyToManyField(TMatch, blank=True)
    teams = models.ManyToManyField(Team, blank=True)

    def __str__(self):
        return ("Bracket number: " + str(self.bracket_num) + " Sub bracket number: " + str(self.sub_bracket_num))

class Week(models.Model):
    week_number = models.IntegerField(null=True, blank=True)
    completed = models.BooleanField(default = False)

    def __str__(self):
        return ("Week " + str(self.week_number))


class League(models.Model):
    title = models.CharField(max_length=50)
    teams = models.ManyToManyField(Team, blank=True)
    matches = models.ManyToManyField(Match, blank=True)
    rounds_per_week = models.IntegerField(null=True, blank=True)
    num_weeks = models.IntegerField(null=True, blank=True)
    meeting_time = models.DateTimeField(null=True, blank=True)
    password = models.CharField(max_length=20, blank=True, null=True)
    brackets = models.ManyToManyField(Bracket, blank=True)
    weeks = models.ManyToManyField(Week, blank=True)
    weeks_completed = models.BooleanField(default=False)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title
