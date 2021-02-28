from django import forms
from account.models import User
from .models import Player

class InstructorCommentForm(forms.Form):
    score = forms.CharField(label='Score', max_length=3)
    comments = forms.CharField(label='Remarks', max_length=1000, required=False)