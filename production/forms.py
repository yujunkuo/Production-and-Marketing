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
    gender_list = ((0, "Male"), (1, "Female"))

    name = forms.CharField(label = '姓名', widget = forms.TextInput)
    gender = forms.ChoiceField(label = '性別', widget = forms.Select(), choices = gender_list, initial = gender_list[0])
    email = forms.EmailField(label = '電子信箱')
    phone = forms.CharField(required = False, label = "電話號碼",  widget = forms.TextInput)
    bday = forms.DateField(label = '出生日期')
    pets = forms.BooleanField(required = False, initial = False, label = '是否有養寵物')
    student = forms.BooleanField(required = False, initial = False, label = '是否為學生')

class expiredStockForm(forms.Form):
    stock_list = []
    i = 0
    for each in Inventory.objects.all():
        stock_list.append([i, each.invName])
        i += 1
    stock = forms.ChoiceField(label = '請選擇欲查詢存貨', widget = forms.Select(), choices = stock_list, initial = stock_list[0])

class provideStockForm(forms.Form):
    name = forms.CharField(label = '存貨', widget = forms.TextInput)
    firm = forms.CharField(label = '廠商', widget = forms.TextInput)
    num = forms.CharField(label = '數量', widget = forms.TextInput)
    expired = forms.DateField(label = '即將到期日')

class provideEquipForm(forms.Form):
    name = forms.CharField(label = '設備', widget = forms.TextInput)
    firm = forms.CharField(label = '廠商', widget = forms.TextInput)
    num = forms.CharField(label = '數量', widget = forms.TextInput)
