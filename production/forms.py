from django import forms
from django.forms import widgets
from production.models import Dish

class orderForm(forms.Form):

    dish_list = []
    i = 0
    for each in Dish.objects.all():
        dish_list.append([i, each.dName])
        i += 1
    mid = forms.CharField(label = '會員ID', widget = forms.TextInput)
    dish = forms.ChoiceField(label = '請選擇欲購買餐點', widget = forms.Select(), choices = dish_list, initial = dish_list[0])
    num = forms.CharField(label = '購買數量', widget = forms.TextInput)
