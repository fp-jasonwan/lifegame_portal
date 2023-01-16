from django.contrib import admin
from booth.models import Booth, Participation, BoothScoring, BoothRequirement, BoothTraffic
# Register your models here.

admin.site.register(Participation)
admin.site.register(BoothScoring)
admin.site.register(BoothRequirement)
admin.site.register(BoothTraffic)

class BoothAdmin(admin.ModelAdmin):
    list_display = ('id', 'booth_in_charge', 'name', 'health_score','academic_score', 'growth_score', 'relationship_score', 'joy_score', 'money')
    filter_horizontal = ('booth_admins',)
    
admin.site.register(Booth, BoothAdmin)