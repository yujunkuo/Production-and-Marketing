from django.shortcuts import render
from django.views.generic import TemplateView
from .forms import orderForm
from datetime import datetime
from production.models import *


def orderSystem(request):
    return render(request, "orderSystem.html")


def memeberJoin(request):
    return render(request, "memeberJoin.html")


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

class JoinView(TemplateView):
    template_name = 'memeberJoin.html'

    def get(self, request):
        global join_form
        join_form = joinForm()
        return render(request, self.template_name, {'form': join_form})

    def post(self, request):
        global join_form
        join_form = joinForm(request.POST)

        if join_form.is_valid():
            mid = int(request.POST.get('mid'))
            name = request.POST.get('Name', "")
            gender = request.POST.get('Gender', "")
            phone = request.POST.get('Phone', "")
            email = request.POST.get('Email', "")
            bday = request.POST.get('BDay', "")
            pets = bool(request.POST.get('Pets', ""))
            student = bool(request.POST.get('Students', ""))
            join_form = joinForm()
        Member.objects.create(MemberID=mid, mName=name, Gender=gender, Phone=phone, Email=email, BDay=bday, Pets=pets
                              , Student=student)
        return render(request, self.template_name, {'form': join_form})


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
            mid = int(request.POST.get('mid'))
            dish = int(request.POST.get('dish'))
            num = int(request.POST.get('num'))
            order_form = orderForm()
            dish_name = Dish.objects.all()[dish]
            time = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')

            try:
                Order.objects.create(oTime=time, MID=Member.objects.get(MemberID=mid),
                                     dishName=Dish.objects.get(dName=dish_name), orderNum=num)
                for i in dish_dict[dish_name]:
                    stock = i
                    stock_db = Inventory.objects.filter(sName=stock).orderby('Expired')
                    used_num = dish_dict[dish_name][i]
            except:
                pass
        return render(request, self.template_name, {'form': order_form, "time": time})


class CheckStockView(TemplateView):

    def get(self, request):
        global check_stock_form
        check_stock_form = checkStockForm()
        return render(request, self.template_name, {'form': check_stock_form})

    def check_stock_all():
        result = Inventory.objects.order_by('Expired')
        return result

    def check_stock_need():
        result = Inventory.objects.get(invNum__lt=20)
        return result

    def check_stock_expired(request):
        name = request.Get.get('Check Stock')
        result = Inventory.objects.get(sName=name).order_by('Expired')
        return result


def check_equip_all():
    result = Equipment.objects.all()
    return result


def check_equip_need():
    result = Equipment.objects.get(eNum__lt=10)
    return result


class ProvideStockView(TemplateView):
    template_name = 'stockProvide.html'

    def get(self, request):
        global provide_stock_form
        provide_stock_form = provideStockForm()
        return render(request, self.template_name, {'form': provide_stock_form})

    def post(self, request):
        global provide_stock_form
        provide_stock_form = provideStockForm(request.POST)

        if provide_stock_form.is_valid():
            name = request.POST.get('Stock Name', "")
            firm = int(request.POST.get('Firm ID'))
            num = int(request.POST.get('Num'))
            expired = request.POST.get('Expired', "")
            provide_stock_form = provideStockForm()

        try:
            Firm.objects.get(FirmID=firm)
        except Firm.DoesNotExist:
            Firm.objects.create(FirmID=firm)

        Inventory.objects.create(invName=name, invNum=num, Expired=expired)
        ProvideInventory.objects.create(piFirm=Firm.objects.get(FirmID=firm), name=Inventory.objects.get(invName=name), piNum=num)

        return render(request, self.template_name, {'form': provide_stock_form})


class ProvideEquipView(TemplateView):
    template_name = 'equipmentProvide.html'

    def get(self, request):
        global provide_equip_form
        provide_equip_form = provideEquipForm()
        return render(request, self.template_name, {'form': provide_equip_form})

    def post(self, request):
        global provide_equip_form
        provide_equip_form = provideEquipFrom(request.POST)

        if provide_equip_form.is_valid():
            name = request.POST.get('Equipment Name', "")
            firm = int(request.POST.get('Frim ID'))
            num = int(request.POST.get('Num'))
            provide_equip_form = provideEquipFrom()

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

        return render(request, self.template_name, {'form': provide_equip_form})


Dish_List = ['拿鐵咖啡', '香草拿鐵', '濃縮咖啡', '卡布奇諾', '焦糖瑪奇朵', '提拉米蘇拿鐵', '貝里斯奶酒咖啡', '特調風味鮮奶茶',
             '玫瑰奶茶', '牛奶糖歐蕾', '可可歐蕾', '抹茶阿法其朵', '蜂蜜檸檬', '蜂蜜奇異果', '精選啤酒', '蘋果優格冰沙', 'Oreo巧克力冰沙',
             '宇治抹茶冰沙', '香蕉巧克力冰沙', '青檸冰紅茶', '玫瑰四物茶', '富士蘋果冰茶', '伯爵紅茶', '烏龍鐵觀音', '日式玄米煎茶',
             '燻火腿芝士夾心焗烤土司', '夏威夷比薩芝士焗烤土司', '原味鬆餅', '焦糖冰淇淋鬆餅', '巧克力冰淇淋鬆餅', '香蕉冰淇淋鬆餅',
             '藍莓貝果', '奶油貝果', '花生貝果', '焦糖北海道牛奶冰淇淋', '甜心草莓冰淇淋', '酥脆巧克力冰淇淋', '起士可頌', '鮪魚可頌',
             '起士火腿可頌', '黑胡椒牛肉可頌', '蔬菜雞肉可頌', '咖喱雞肉皮塔', '辣味牛肉皮塔', '法式鴨胸皮塔', '挪威燻鮭魚沙拉',
             '燻火腿沙拉', '一杯雞蛋沙拉（素）', '一杯鮪魚沙拉']


def prediction(request):
    name = request.Get.get('Dish name')
    curr = datetime.datetime.now()
    num_per_month = []
    predict_for_month = []

    dish_order = Order.objects.filter(dishName=name)
    for year in range(2019, curr.year + 1):
        if year != curr.year:
            for month in range(1, 13):
                count = 0
                for ds_order in dish_order:
                    if ds_order.oTime.year == year and ds_order.oTime.month == month:
                        count += ds_order.orderNum
                num_per_month.append(count)
        else:
            for month in range(1, curr.month + 1):
                count = 0
                for ds_order in dish_order:
                    if ds_order.oTime.year == year and ds_order.oTime.month == month:
                        count += ds_order.orderNum
                num_per_month.append(count)
        predict_for_month.append(num_per_month[0])

    for i in range(len(num_per_month) - 1):
        predict = predict_for_month[i] + 0.15 * (num_per_month[i + 1] - predict_for_month[i])
        predict_for_month.append(predict)

    return name, predict_for_month[-1]