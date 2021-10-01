from django import Form


class ReportScore(forms.Form):
    team1_score = IntegerField(min_value=0, max_value=3, initial="0")
    team2_score = IntegerField(min_value=0, max_value=3, initial="0")
