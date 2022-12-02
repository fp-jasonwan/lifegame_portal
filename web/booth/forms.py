from django import forms
from account.models import User
from booth.models import Booth, BoothScoring, Participation
from django.forms import ModelForm
class ParticipationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ParticipationForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
           visible.field.widget.attrs['class'] = 'usernameBox form-control'

    # user_id = forms.IntegerField(label='User ID')
    # booth_id = forms.CharField(label='Booth ID', max_length=3)
    # booth_score_id = forms.IntegerField(label='Score ID')
    # remarks = forms.CharField(label='Remarks', max_length=200, required=False)

    class Meta:
        model = Participation
        fields = '__all__'
