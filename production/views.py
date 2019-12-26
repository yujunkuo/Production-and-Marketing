from django.shortcuts import render
from django.views.generic import TemplateView
from .forms import orderForm
import datetime
from production.models import *


def orderSystem(request):
    return render(request, "orderSystem.html")

def checkSystem(request):
    return render(request, "checkSystem.html")

def provideSystem(request):
    return render(request, "provideSystem")

def stockCheck(request):
    return render(request, "stockCheck.html")

def equipmentCheck(request):
    return render(request, "equipmentCheck.html")

def stockProvide(request):
    return render(request, "stockProvide.html")

def equipmentProvide(request):
    return render(request, "equipmentProvide.html")

dish_dict = {'拿鐵咖啡': {'牛奶': 1, '咖啡': 1}, '巧克力冰淇淋鬆餅': {'巧克力': 1, '冰淇淋': 1, '鬆餅粉': 1},
             '挪威燻鮭魚沙拉': {'鮭魚': 1, '萵苣': 2, '番茄': 3, '麵包丁': 2, '沙拉醬': 1}}

# Create your views here.
def join_member(request):
    Member.objects.create(mName=name, Gender=gender, Phone=phone, Email=email, BDay=bday, Pets=pets
                          , Student=student, MemberID=id)
    '''if Member.objects.filter(mName__isnull = True):
        members=Member.objects.filter(mName__isnull = True)
        member_choose = members[0]
        member_choose.Name = name
        member_choose.Gender = gender
        member_choose.Phone = phone
        member_choose.Email = email
        member_choose.BDay = bday
        member_choose.Pets = pets
        member_choose.Students = student
        member_choose.save()
    else:
        Member.objects.create(mName=name, Gender=gender, Phone=phone, Email=email, BDay=bday, Pets=pets
                              , Student=student)'''
    new_member = Member.objects.get(MemberID=id)
    return new_member

class OrderView(TemplateView):

    template_name = 'orderSystem.html'

    def get(self, request):
        global order_form
        order_form = orderForm()
        return render(request, self.template_name, {'form': order_form})

    def post(self, request):
        global order_form
        order_form = orderForm(request.POST)

        if order_form.is_valid():
            mid = request.POST.get('mid', "")
            dish = request.POST.get('dish', "")
            num = request.POST.get('num', "")
            order_form = orderForm()

            try:
                mid = Member.objects.get(MemberID=mid)
                Order.objects.create(oTime=time, MID=Member.objects.get(MemberID=mid),
                                     dishName=Dish.objects.get(dName=dish), orderNum=num)
                for i in dish_dict[dish]:
                    stock = i
                    stock_db = Stock.objects.filter(sName=stock).orderby('Expired')
                    used_num = dish_dict[dish][i]
            except:
                pass
        return render(request, self.template_name, {'form': order_form})

def check_stock_all():
    result = Stock.objects.order_by('Expired')
    return result


def check_stock_expired(request):
    name = request.Get.get('Check Stock')
    result = Stock.objects.get(sName=name).order_by('Expired')
    return result


def check_equip_all():
    result = Equipment.objects.all()
    return result


def check_stock_need():
    result = Stock.objects.get(sNum__lt=20)
    return result


def check_equip_need():
    result = Equipment.objects.get(eNum__lt=10)
    return result


def provide_stock(x: str, y: int, z: datetime, w: int, p: int):
    # name = request.Get.get('Provide Stock Name')
    # firm = request.Get.get('Provide Stock Firm')
    # num = request.Get.get('Provide Stock Num')
    # expired = request.Get.get('Stock Expired Date')
    name = x
    firm = y
    expired = z
    num = w

    try:
        Firm.objects.get(FirmID=firm)
    except Firm.DoesNotExist:
        Firm.objects.create(FirmID=firm)

    Stock.objects.create(sName=name, sNum=num, Expired=expired)
    ProvideStock.objects.create(psFirm=Firm.objects.get(FirmID=firm),name=Stock.objects.get(sName=name),psNum=num)

    SuccessMSG = 'Successfully Update Stock'
    return SuccessMSG


def provide_equip(request):
    name = request.Get.get('Provide Equipment Name')
    firm = request.Get.get('Provide Equipment Firm')
    num = request.Get.get('Provide Equipment Num')

    try:
        Firm.objects.get(FirmID=firm)
    except Firm.DoesNotExit:
        Firm.objects.create(FirmID=firm)

    try:
        Equipment.objects.get(eName=name)
    except Equipment.DoesNotExit:
        Equipment.objects.create(eName=name, eNum=0)

    equip = Equipment.objects.get(eName=name)
    origin_num = equip.eNum
    new_num = origin_num + num
    equip.eNum = new_num
    equip.save()

    ProvideEquip.objects.create(peFirm=Firm.objects.get(FirmID=firm), pEquip=Equipment.objects.get(eName=name)
                                , peNum=num)

    success_msg = 'Successfully Update Equipment'
    return success_msg
