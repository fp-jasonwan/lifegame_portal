from django import forms
from account.models import User
from .models import Player

class InstructorCommentForm(forms.Form):
    score = forms.CharField(label='分數', max_length=3)
    comments = forms.CharField(label='評價', max_length=1000, required=False)