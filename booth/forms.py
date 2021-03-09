from django import forms
from account.models import User
from booth.models import Booth, BoothScoring
from django.forms import ModelForm
from django_toggle_switch_widget.widgets import DjangoToggleSwitchWidget

class ParticipationForm(forms.Form):
    user_id = forms.IntegerField(label='User ID')
    booth_id = forms.CharField(label='Booth ID', max_length=3)
    booth_score_id = forms.IntegerField(label='Score ID')
    remarks = forms.CharField(label='Remarks', max_length=200, required=False)


class TestModelForm(ModelForm):
    class Meta:
        model = Booth
        fields = "__all__"
        widgets = {
            "is_active": DjangoToggleSwitchWidget(klass="django-toggle-switch-dark-primary"),
        }