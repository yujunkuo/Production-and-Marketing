from django import forms
from production.views import OrderView

class OrderForm(forms.Form):
    memID = forms.CharField(label='內容', widget=forms.Textarea)
    order = forms.ChoiceField
