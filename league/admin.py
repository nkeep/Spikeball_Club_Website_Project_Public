from django.contrib import admin
from .models import League, Match, Team, Bracket, TMatch, Week

# Register your models here.
admin.site.register(Team)
admin.site.register(League)
admin.site.register(Match)
admin.site.register(TMatch)
admin.site.register(Bracket)
admin.site.register(Week)
