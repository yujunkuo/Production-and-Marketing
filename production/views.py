from django.shortcuts import render
from django.views.generic import TemplateView
from .forms import orderForm
from .forms import joinMemberForm
from .forms import provideStockForm
from .forms import provideEquipForm
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

def prediction(request):
    return render(request, "prediction.html")

dish_dict = {'拿鐵咖啡': {'牛奶': 1, '咖啡': 1}, '巧克力冰淇淋鬆餅': {'巧克力': 1, '冰淇淋': 1, '鬆餅粉': 1},
             '挪威燻鮭魚沙拉': {'鮭魚': 1, '萵苣': 2, '番茄': 3, '麵包丁': 2, '沙拉醬': 1}}

# Create your views here.
class JoinMemberView(TemplateView):
    template_name = 'memberJoin.html'
    def get(self, request):
        global join_member_form
        join_member_form = joinMemberForm()
        return render(request, self.template_name, {'form': join_member_form })

    def post(self, request):
        global join_member_form
        join_member_form = joinMemberForm(request.POST)
        if join_member_form.is_valid():
            name = request.POST.get('name', "")
            gender = "Female" if request.POST.get('gender', "") else "Male"
            email = request.POST.get('email', "")
            phone = request.POST.get('phone', "")
            bday = request.POST.get('bday', "")
            pets = True if (request.POST.get('pets', "") == "on") else False
            student = True if (request.POST.get('student', "") == "on") else False
            join_member_form = joinMemberForm()
            member_id = Member.objects.order_by('MemberID').last().MemberID + 1

            Member.objects.create(mName=name, Gender=gender, Phone=phone, Email=email, BDay=bday, Pets=pets
                                    , Student=student, MemberID=member_id)
            new_member = Member.objects.order_by('MemberID').last()

            return render(request, self.template_name, {
                    'form': join_member_form,
                    'res': "恭喜 " + new_member.mName + " 已成為會員"
                    })
        else:
            return render(request, self.template_name, {
                    'form': join_member_form,
                    'res': "表單驗證失敗，無法加入會員"
                    })

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
            order_id = Order.objects.order_by('oID').last().oID + 1

            Order.objects.create(oID=order_id, oTime=time, MID=Member.objects.get(MemberID=mid),
                                 dishName=Dish.objects.get(dName=dish_name), orderNum=num)
            dish_name_str = str(dish_name)
            if dish_name_str in dish_dict:
                for need_inv in dish_dict[dish_name_str]:
                    need_num = num * dish_dict[dish_name_str][need_inv]
                    if Made.objects.filter(madeID=1):
                        made_id = Made.objects.order_by('madeID').last().madeID + 1
                    else:
                        made_id = 1
                    mtime = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
                    Made.objects.create(madeID=made_id, mTime=mtime, mDish=Dish.objects.get(dName=dish_name_str)
                                        , mInvent=Inventory.objects.filter(invName=need_inv).first(), mNum=need_num)
                    for inv in Inventory.objects.filter(invName=need_inv).order_by('Expired'):
                        if need_num <= inv.invNum:
                            inv.invNum -= need_num
                            inv.save()
                            break
                        else:
                            need_num -= inv.invNum
                            inv.invNum = 0
                            inv.save()
                if Inventory.objects.filter(invNum=0):
                    zero_inv = Inventory.objects.filter(invNum=0)
                    zero_inv.delete()
            else:
                pass
        print(abc)
        return render(request, self.template_name, {'form': order_form, "time": time})

inventory_minimum = {'牛奶': 50, '咖啡': 100, '巧克力': 50, '冰淇淋': 40, '鬆餅粉': 50, '鮭魚': 30, '萵苣': 45, '番茄': 45,
                     '麵包丁': 35, '沙拉醬': 50, 'egg' : 100}


class CheckStockAllView(TemplateView):
    def get(self, request):
        inv_all_name = []
        inv_all_num = []
        inv_all_expired = []
        result = Inventory.objects.order_by('Expired')
        result = list(result)
        for each in result:
            inv_all_name.append(each.invName)
            inv_all_num.append(each.invNum)
            time = each.Expired
            expired = time.isoformat()
            inv_all_expired.append(expired)
        return render(request, 'stockCheck.html',{
            "inv_all_name": inv_all_name,
            "inv_all_num": inv_all_num,
            "inv_all_expired": inv_all_expired,
                })

class CheckStockNeedView(TemplateView):
    def get(self, request):
        need_inventory = []

        all_inventory = Inventory.objects.values('invName').distinct()
        for i in all_inventory:
            name = i['invName']
            num = 0
            inventory = Inventory.objects.filter(invName=name)
            for inv in inventory:
                num += inv.invNum
                if num <= inventory_minimum[name]:
                    need = str(name) + ' : ' + str(num) + '份 (至少需要' + str(inventory_minimum[name]) + '份）'
                    need_inventory.append(need)
        return render(request, 'stockCheck.html', {
                "need_inventory" : need_inventory
        })

class CheckStockExpiredView(TemplateView):
    def get(self, request):
        name = request.Get.get('Check Stock')
        inv_expired_name = []
        inv_expired_num = []
        inv_expired_time = []
        result = Inventory.objects.get(sName=name).order_by('Expired')
        result = list(result)
        for each in result:
            inv_expired_name.append(each.invName)
            inv_expired_num.append(each.invNum)
            inv_expired_time.append(each.Expired)
        return render(request, "stockCheck.html", {
                "inv_expired_name" : inv_expired_name,
                "inv_expired_num" : inv_expired_num,
                "inv_expired_time" : inv_expired_time,
        })



class CheckEquipAllView(TemplateView):
    def get(self, request):
            result = Equipment.objects.all()
            equip_all_name = []
            equip_all_num = []
            result = list(result)
            for each in result:
                equip_all_name.append(each.eName)
                equip_all_num.append(each.eNum)
            return render(request, "equipmentCheck.html", {
                    "equip_all_name" : equip_all_name,
                    "equip_all_num" : equip_all_num,
            })

class CheckEquipNeedView(TemplateView):
    def get(self, request):
        result = Equipment.objects.get(eNum__lt=10)
        equip_need_name = []
        equip_need_num = []
        result = list(result)
        for each in result:
            equip_need_name.append(each.eName)
            equip_need_num.append(each.eNum)
        return render(request, "equipmentCheck.html"), {
                "equip_need_name" : equip_need_name,
                "equip_need_num" : equip_need_num,
    }



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
            name = request.POST.get('name')
            firm = int(request.POST.get('firm'))
            num = int(request.POST.get('num'))
            expired = request.POST.get('expired')
            provide_stock_form = provideStockForm()

        try:
            Firm.objects.get(FirmID=firm)

        except Firm.DoesNotExist:
            Firm.objects.create(FirmID=firm)

        inventory_id = Inventory.objects.order_by('invID').last().invID + 1
        Inventory.objects.create(invID=inventory_id, invName=name, invNum=num, Expired=expired)
        ProvideInventory.objects.create(piFirm=Firm.objects.get(FirmID=firm), pInvent=Inventory.objects.get(invID=inventory_id), piNum=num)

        return render(request, self.template_name, {'form': provide_stock_form})

class ProvideEquipView(TemplateView):
    template_name = 'equipmentProvide.html'

    def get(self, request):
        global provide_equip_form
        provide_equip_form = provideEquipForm()
        return render(request, self.template_name, {'form': provide_equip_form})

    def post(self, request):
        global provide_equip_form
        provide_equip_form = provideEquipForm(request.POST)

        if provide_equip_form.is_valid():
            name = request.POST.get('name')
            firm = int(request.POST.get('firm'))
            num = int(request.POST.get('num'))
            provide_equip_form = provideEquipForm()

        try:
            Firm.objects.get(FirmID=firm)
        except:
            Firm.objects.create(FirmID=firm)
        else:
            pass

        try:
             Equipment.objects.get(eName=name)
        except:
            Equipment.objects.create(eName=name, eNum=0)
        else:
            pass

        equip = Equipment.objects.get(eName=name)
        origin_num = equip.eNum
        new_num = origin_num + num
        equip.eNum = new_num
        equip.save()

        ProvideEquip.objects.create(peFirm=Firm.objects.get(FirmID=firm), pEquip=Equipment.objects.get(eName=name), peNum=num)

        return render(request, self.template_name, {'form': provide_equip_form})


Dish_List = ['拿鐵咖啡', '香草拿鐵', '濃縮咖啡', '卡布奇諾', '焦糖瑪奇朵', '提拉米蘇拿鐵', '貝里斯奶酒咖啡', '特調風味鮮奶茶',
             '玫瑰奶茶', '牛奶糖歐蕾', '可可歐蕾', '抹茶阿法其朵', '蜂蜜檸檬', '蜂蜜奇異果', '精選啤酒', '蘋果優格冰沙', 'Oreo巧克力冰沙',
             '宇治抹茶冰沙', '香蕉巧克力冰沙', '青檸冰紅茶', '玫瑰四物茶', '富士蘋果冰茶', '伯爵紅茶', '烏龍鐵觀音', '日式玄米煎茶',
             '燻火腿芝士夾心焗烤土司', '夏威夷比薩芝士焗烤土司', '原味鬆餅', '焦糖冰淇淋鬆餅', '巧克力冰淇淋鬆餅', '香蕉冰淇淋鬆餅',
             '藍莓貝果', '奶油貝果', '花生貝果', '焦糖北海道牛奶冰淇淋', '甜心草莓冰淇淋', '酥脆巧克力冰淇淋', '起士可頌', '鮪魚可頌',
             '起士火腿可頌', '黑胡椒牛肉可頌', '蔬菜雞肉可頌', '咖喱雞肉皮塔', '辣味牛肉皮塔', '法式鴨胸皮塔', '挪威燻鮭魚沙拉',
             '燻火腿沙拉', '一杯雞蛋沙拉（素）', '一杯鮪魚沙拉']

class PedictionView(TemplateView):
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
