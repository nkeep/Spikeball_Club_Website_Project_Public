from django import forms

class LeagueScoreReport(forms.Form):
    score1 = forms.IntegerField()
    score2 = forms.IntegerField()
    game_no = forms.IntegerField()
    match_id = forms.IntegerField()
