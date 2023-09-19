from django import forms

class textForm(forms.Form):
   text_input = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}), max_length=100000)