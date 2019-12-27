from django import forms
from django.forms import widgets
from production.models import *

class orderForm(forms.Form):

    dish_list = []
    i = 0
    for each in Dish.objects.all():
        dish_list.append([i, each.dName])
        i += 1
    mid = forms.CharField(label = '會員ID', widget = forms.TextInput)
    dish = forms.ChoiceField(label = '請選擇欲購買餐點', widget = forms.Select(), choices = dish_list, initial = dish_list[0])
    num = forms.CharField(label = '購買數量', widget = forms.TextInput)

class joinMemberForm(forms.Form):
    name = forms.CharField(max_length = 5, label = '姓名', widget = forms.TextInput)
    gender = forms.CharField(label = '性別', widget = forms.TextInput)
    email = forms.EmailField(label = '電子信箱', widget = forms.TextInput)
    phone = forms.CharField(required = False, label = "電話號碼",  widget = forms.TextInput)
    bday = forms.DateField(label = '出生日期', error_messages = { 'invalid' : '輸入的生日日期無效'})
    pets = forms.BooleanField(required = False, initial = False, label = '是否有養寵物')
    student = forms.BooleanField(required = False, initial = False, label = '是否為學生')
