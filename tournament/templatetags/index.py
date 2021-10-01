from django import template
register = template.Library()

@register.filter
def index(indexable, i):
    return indexable.matches.get(match_number=i)

@register.filter
def team(indexable, i):
    if(i==1):
        return indexable.team1
    elif(i==2):
        return indexable.team2

@register.filter
def winner(match):
    if match.winner == 1:
        return 1

@register.filter
def score(indexable, i):
    if(i==1):
        return indexable.team1_score
    elif(i==2):
        return indexable.team2_score
