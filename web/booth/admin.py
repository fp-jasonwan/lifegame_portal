from django.contrib import admin
from booth.models import Booth, Participation, Transaction, BoothScoring, BoothRequirement, BoothTraffic
# Register your models here.



admin.site.register(BoothScoring)
admin.site.register(BoothRequirement)
admin.site.register(BoothTraffic)

class BoothAdmin(admin.ModelAdmin):
    list_display = ('id', 'booth_in_charge', 'name', 'health_score','skill_score', 'growth_score', 'relationship_score', 'money')
    filter_horizontal = ('booth_admins',)
admin.site.register(Booth, BoothAdmin)


class ParticipationAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_select_related = True
    list_display = ('id', 'booth', 'player', 'record_time', 'score' )
    search_fields = ['player__user__username']
    raw_id_fields = ['player', 'booth']
    ordering = ['player__user__id']
admin.site.register(Participation, ParticipationAdmin)

class TransactionAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_select_related = True
    list_display = ('id', 'booth', 'player', 'record_time', 'type', 'money')
    search_fields = ['player__user__username']
    raw_id_fields = ['player', 'booth']
    ordering = ['player__user__id']
admin.site.register(Transaction, TransactionAdmin)