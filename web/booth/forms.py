from django import forms
from account.models import User
from booth.models import Booth, BoothScoring, Participation, Transaction
from player.models import Player
from django.forms import ModelForm

class ParticipationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ParticipationForm, self).__init__(*args, **kwargs)
        booth = kwargs['initial']['booth']
        self.fields['score'].queryset = booth.score_options
        for visible in self.visible_fields():
           visible.field.widget.attrs['class'] = 'usernameBox form-control'        

    class Meta:
        model = Participation
        fields = '__all__'

class TransactionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TransactionForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
           visible.field.widget.attrs['class'] = 'usernameBox form-control'        

    class Meta:
        model = Transaction
        fields = '__all__'

class BoothSettingsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BoothSettingsForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
           visible.field.widget.attrs['class'] = 'usernameBox form-control'
        
    class Meta:
        model = Booth
        fields = ['health_score', 'growth_score', 'relationship_score', 'skill_score', 'money']