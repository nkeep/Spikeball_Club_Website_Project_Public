from django import template
from django.contrib.humanize.templatetags.humanize import ordinal
register = template.Library()

@register.filter
def bracket_name(i):
    lower = 2**(i-1) + 1
    upper = 2**i
    return ("for " + ordinal(lower) + "-" + ordinal(upper) + " place")

@register.filter
def week_complete(indexable, i):
    week = indexable.weeks.get(week_number = i)
    if week.completed:
        return True
    else:
        return False

@register.filter
def week(indexable, i):
    return indexable.matches.filter(week_number=i)

@register.filter
def round(indexable, i):
    return indexable.filter(round_number=i)

@register.filter
def bracket(indexable, i):
    return indexable.brackets.get(pk=i)

@register.filter
def tround(indexable, i):
    return indexable.matches.filter(round_number=i)

@register.filter
def completed(indexable):
    for match in indexable:
        if not match.winner1 and not match.winner2 and not match.winner3:
            return False
    return True
