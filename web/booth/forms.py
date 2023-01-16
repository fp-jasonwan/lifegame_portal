from django import forms
from account.models import User
from booth.models import Booth, BoothScoring, Participation
from player.models import Player
from django.forms import ModelForm

class ParticipationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ParticipationForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
           visible.field.widget.attrs['class'] = 'usernameBox form-control'        
    booth = forms.ModelChoiceField(queryset=Booth.objects.all())
    player = forms.ModelChoiceField(queryset=Player.objects.all())
    marker = forms.ModelChoiceField(queryset=User.objects.all())

    class Meta:
        model = Participation
        fields = '__all__'

class BoothSettingsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BoothSettingsForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
           visible.field.widget.attrs['class'] = 'usernameBox form-control'
        
    class Meta:
        model = Booth
        fields = ['joy_score', 'health_score', 'growth_score', 'relationship_score', 'academic_score', 'money']