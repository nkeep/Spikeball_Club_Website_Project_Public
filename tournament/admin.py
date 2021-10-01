from django.contrib import admin
from django.utils.html import format_html
from .models import TTeam, TMatch, Tournament, Pool, PMatch, PRound, PaymentOption

class TournamentAdmin(admin.ModelAdmin):
    list_display = ('name', 'payment_page',)

    def payment_page(self, obj):
        return format_html('<a href="{url}">Payment Page</a>', url=f"https://stoutspikers.herokuapp.com/tournament/tournamentpayments/{obj.pk}")

# Register your models here.
admin.site.register(TTeam)
admin.site.register(TMatch)
admin.site.register(Tournament, TournamentAdmin)
admin.site.register(Pool)
admin.site.register(PMatch)
admin.site.register(PRound)
admin.site.register(PaymentOption)
