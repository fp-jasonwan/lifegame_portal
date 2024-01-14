from django import forms
from account.models import User
from booth.models import Booth, BoothScoring, Participation, Transaction
from player.models import Player
from django.forms import ModelForm
import datetime

class ParticipationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ParticipationForm, self).__init__(*args, **kwargs)
        booth = kwargs['initial']['booth']
        # self.fields['score'].queryset = booth.score_options
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
        self.fields['health_score'].label = '健康指數'
        self.fields['skill_score'].label = '技能指數'
        self.fields['growth_score'].label = '成長指數'
        self.fields['relationship_score'].label = '關係指數'
        self.fields['academic_level'].label = '學歷'
        self.fields['money'].label = '金錢'
        
    class Meta:
        model = Booth
        fields = ['health_score', 'growth_score', 'relationship_score', 'skill_score', 'academic_level', 'money']