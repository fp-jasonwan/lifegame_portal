from django.contrib import admin
from player.models import Player, Education, BornStatus, InstructorScore
# Register your models here.

# admin.site.register(Player)
admin.site.register(Education)
admin.site.register(BornStatus)

class PlayerAdmin(admin.ModelAdmin):
    list_display = ('user', 'born_status', 'born_education_level')
    actions = ['deactivate_player',]

    def deactivate_player(self, request, queryset):
        queryset.update(live_status='inactive')
        queryset.update(past_user=queryset.user)
        queryset.update(user=null)
admin.site.register(Player, PlayerAdmin)
admin.site.register(InstructorScore)