from django import forms

# 創建表單
class CustomerForm(forms.Form):
    file = forms.FileField()