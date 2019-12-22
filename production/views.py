from django.shortcuts import render
import datetime
from production.models import *


# Create your views here.
def order(request):
    odertime = datetime.datetime.now()
    mID = request.Get.get('Member ID')
    dish = request.Get.get('Dish_Name')
    num = request.Get.get('Dish num')
    try:
        mID = Member.objects.get(MemberID=mID)

        Order.objects.create(oTime=odertime, MemberID=mID, dName='dish', oNum=num)
        SuccessMSG = 'Finish Ordering'
        return SuccessMSG
    except:
        Errormessage = 'Please join our membership'
        return Errormessage


def Made(request):
    madeTime = datetime.datetime.now()
    dName = request.Get.get('Dish Name')


def checkStockAll():
    result = Stock.objects.order_by('Expired')
    return result


def checkEquipAll():
    result = Equipment.objects.all()
    return result


def checkStockNeed():
    result = Stock.objects.get(sNum < 20)
    return result


def checkEquipNeed():
    result = Equipment.objects.get(eNum < 10)
    return result


def ProvideStock(request):
    time = datetime.datetime.now()
    name = request.Get.get('Provide Stock Name')
    firm = request.Get.get('Provide Stock Firm')
    num = request.Get.get('Provide Stock Num')
    expired = request.Get.get('Stock Expired Date')

    try:
        firm = Firm.objects.get(FirmID=firm)
        ProvideStock.objects.create(psTime=time, psName=name, psFirm=firm, psNum=num)

        Stock.objects.create(sName=name, sNum=num, Expired=expired, )  # 要加sPrice

        SuccessMSG = 'Successfully Update Stock'
        return SuccessMSG

    except:
        ErrorMSG = 'Cannot find this firm! Please create a new FirmID'
        return ErrorMSG


def ProvideEquip(request):
    time = datetime.datetime.now()
    name = request.Get.get('Provide Equipment Name')
    firm = request.Get.get('Provide Equipment Firm')
    num = request.Get.get('Provide Equipment Num')

    try:
        firm = Firm.objects.get(FirmID=firm)

        ProvideEquip.objects.create(peTime=time, peName=name, peFirm=firm, peNum=num)
        equip = Equipment.objects.get(eName=name)
        equip.eNum += num
        equip.save()

        SuccessMSG = 'Successfully Update Equipment'
        return SuccessMSG

    except:
        Errormessage = 'Cannot find this firm! Please create a new FirmID'
        return Errormessage
