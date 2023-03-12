from django.contrib import admin
from django import forms
from player.models import Player, BornStatus, InstructorScore

# Register your models here.
class PlayerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PlayerForm, self).__init__(*args, **kwargs)
        self.fields['user'].queryset = self.fields['user'].queryset.order_by('id')

    class Meta:
      model = Player
      fields = '__all__'
    field_order = ['user']
    #   fields = ("nbr", "store", "created", "last_change")

class PlayerAdmin(admin.ModelAdmin):
    list_per_page = 10
    search_fields = ['user__id']
    form = PlayerForm
    ordering = ['user__id']
    

admin.site.register(Player, PlayerAdmin)
admin.site.register(BornStatus)
