from django import forms
from django.contrib.auth.models import User

from .models import PostComment

class CommentForm(forms.ModelForm):
    comment = forms.CharField(widget = forms.TextInput(attrs={'cols':120,'placeholder':'Add comment...'}),label='')
    class Meta:
        model = PostComment
        fields = ['comment']