from django.shortcuts import render
import datetime
from production.models import *

def orderSystem(request):
    return render(request, "orderSystem.html")

def inventorySystem(request):
    return render(request, "inventorySystem.html")
    
def equipmentSystem(request):
    return render(request, "equipmentSystem.html")

# Create your views here.
def order(x : int, y : str, z : int, w : datetime):
    '''
    mid = request.Get.get('Member ID')
    dish = request.Get.get('Dish_Name')
    num = request.Get.get('Dish num')
    '''
    mid = x
    dish = y
    num = z
    time = w

    try:
        mid = Member.objects.get(MemberID=mid)
    except Member.DoesNotExit:
        Member.objects.create(MemberID=mid)

    Order.objects.create(oTime = time, MemberID=Member.objects.get(MemberID=mid),
                         dName=Dish.objects.get(dName=dish), oNum=num)
    success_msg = 'Finish Ordering'
    return success_msg


def made(request):
    made_time = datetime.datetime.now()
    d_name = request.Get.get('Dish Name')


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
    price = p

    try:
        Firm.objects.get(FirmID=firm)
        Stock.objects.get(sName=name)

    except Firm.DoesNotExist:
        Firm.objects.create(FirmID=firm)

    '''except Stock.DoesNotExist:
        print("Remember to update stock's price")'''

    Stock.objects.create(sName=name, sNum=num, Expired=expired, sPrice=price)
    ProvideStock.objects.create(psFirm=Firm.objects.get(FirmID=firm), name=Stock.objects.get(sName=name),
                                psNum=num)

    SuccessMSG = 'Successfully Update Stock'
    return SuccessMSG


def provide_equip(request):
    name = request.Get.get('Provide Equipment Name')
    firm = request.Get.get('Provide Equipment Firm')
    num = request.Get.get('Provide Equipment Num')
    price = request.Get.get('Equipment Price')

    try:
        Firm.objects.get(FirmID=firm)
    except Firm.DoesNotExit:
        Firm.objects.create(FirmID=firm)

    try:
        Equipment.objects.get(eName=name)
    except Equipment.DoesNotExit:
        Equipment.objects.create(eName=name, eNum=0, ePrice=price)

    equip = Equipment.objects.get(eName=name)
    origin_num = equip.eNum
    new_num = origin_num + num
    equip.eNum = new_num
    equip.save()

    ProvideEquip.objects.create(peFirm=Firm.objects.get(FirmID=firm), pEquip=Equipment.objects.get(eName=name)
                                , peNum=num)

    success_msg = 'Successfully Update Equipment'
    return success_msg
