from django import forms
from django.forms import widgets

class orderForm(forms.Form):
    mid = forms.CharField(label = '會員ID', widget = forms.TextInput)
    dish = forms.ChoiceField(label = '請選擇欲購買餐點', widget = forms.Select)
    num = forms.CharField(label = '購買數量', widget = forms.TextInput)
