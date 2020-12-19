from django.contrib import admin
from booth.models import Booth, Participation, BoothScoring
# Register your models here.

admin.site.register(Participation)
admin.site.register(BoothScoring)

class BoothAdmin(admin.ModelAdmin):
    list_display = ('id', 'booth_in_charge', 'name')
    filter_horizontal = ('booth_admins',)

admin.site.register(Booth, BoothAdmin)