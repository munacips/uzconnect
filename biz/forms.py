from attr import field
from django import forms
from .models import Good, Service


class PostBizForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['service','estimate_prize','phone_or_whatsapp_number','description','feature_pic']


class PostProductForm(forms.ModelForm):
    class Meta:
        model = Good
        fields = ['good','estimate_prize','phone_or_whatsapp_number','description','feature_pic']

class SearchForm(forms.Form):
    search = forms.CharField(widget = forms.TextInput(attrs={'placeholder':'Search...'}),label='')