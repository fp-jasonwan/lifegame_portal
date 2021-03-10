from django import forms
from account.models import User
from booth.models import Booth, BoothScoring
from django.forms import ModelForm
class ParticipationForm(forms.Form):
    user_id = forms.IntegerField(label='User ID')
    booth_id = forms.CharField(label='Booth ID', max_length=3)
    booth_score_id = forms.IntegerField(label='Score ID')
    remarks = forms.CharField(label='Remarks', max_length=200, required=False)

