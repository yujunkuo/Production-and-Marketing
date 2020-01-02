from django.shortcuts import render
from django.views.generic import TemplateView

from .forms import CustomerForm
from production.models import Member, Dish, Order

# Kmeans packages
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from datetime import datetime

# Decision Tree packages
from sklearn import tree
import graphviz
import pydotplus
from sklearn.externals.six import StringIO

from io import BytesIO
import base64

from django.http import HttpResponse


# Create your views here.

def main(request):
    return render(request, 'main.html')


def members(request):
    return render(request, 'members.html')


def swot(request):
    return render(request, 'swot.html')


class STPView(TemplateView):
    def get(self, request):
        pre = DecisionTreeView.decision_tree_calculate(DecisionTreeView)
        res = []
        for i in range(len(pre)):
            if pre[i] == "High":
                target = ""
                if i < 4:
                    target += "沒有養寵物、"
                else:
                    target += "有養寵物、"
                if i in [0, 1, 4, 5]:
                    target += "不是學生、"
                else:
                    target += "是學生、"
                if i % 2 == 0:
                    target += "女生 "
                else:
                    target += "男生 "
                res.append(target)

        return render(request, 'stp.html', {"res": res})


class RFMView(TemplateView):
    def get(self, request):
        id_list = []
        name_list = []
        email_list = []
        for cust in Member.objects.all():
            id_list.append(cust.MemberID)
            name_list.append(cust.mName)
            email_list.append(cust.Email)
        r, f, m = [None] * len(id_list), [None] * len(id_list), [None] * len(id_list)
        df = pd.DataFrame({"id": id_list, "name": name_list, "email": email_list, "R": r, "F": f, "M": m})
        # The Recency Score of RFM
        rec = []
        rec_set = set()
        for order in Order.objects.all().order_by('-oTime'):
            if order.MID.MemberID not in rec_set:
                rec.append(order.MID.MemberID)
                rec_set.add(order.MID.MemberID)
        for cust in Member.objects.all():
            if cust.MemberID not in rec_set:
                rec.append(cust.MemberID)
        for id in rec[:int(len(rec) / 3)]:
            df.loc[df["id"] == id, "R"] = 3
        for id in rec[int(len(rec) / 3):int(len(rec) * 2 / 3)]:
            df.loc[df["id"] == id, "R"] = 2
        for id in rec[int(len(rec) * 2 / 3):]:
            df.loc[df["id"] == id, "R"] = 1
        # The Frequency Score of RFM
        freq = {}
        for cust in Member.objects.all():
            order_list = Order.objects.filter(MID=cust.MemberID)
            times = len(order_list)
            freq[cust.MemberID] = times
        freq_res = sorted(freq.items(), key=lambda item: item[1], reverse=True)
        for each in freq_res[:int(len(freq_res) / 3)]:
            df.loc[df["id"] == each[0], "F"] = 3
        for each in freq_res[int(len(freq_res) / 3):int(len(freq_res) * 2 / 3)]:
            df.loc[df["id"] == each[0], "F"] = 2
        for each in freq_res[int(len(freq_res) * 2 / 3):]:
            df.loc[df["id"] == each[0], "F"] = 1
        # The Monetary Score of RFM
        mon = {}
        for cust in Member.objects.all():
            cons = 0
            orders = Order.objects.filter(MID=cust.MemberID)
            for order in orders:
                dish = Dish.objects.filter(dName=order.dishName)
                dish_price = dish[0].dPrice
                cons += dish_price
            mon[cust.MemberID] = cons
        mon_res = sorted(mon.items(), key=lambda item: item[1], reverse=True)
        for each in mon_res[:int(len(mon_res) / 3)]:
            df.loc[df["id"] == each[0], "M"] = 3
        for each in mon_res[int(len(mon_res) / 3):int(len(mon_res) * 2 / 3)]:
            df.loc[df["id"] == each[0], "M"] = 2
        for each in mon_res[int(len(mon_res) * 2 / 3):]:
            df.loc[df["id"] == each[0], "M"] = 1

        vip = df[(df["R"] == 3) & (df["F"] == 3) & (df["M"] == 3)]
        welcome = df[(df["R"] == 3) & (df["F"] == 1)]
        old = df[(df["R"] == 1) & (df["F"] == 3) & (df["M"] == 3)]
        delete = df[(df["R"] == 1) & (df["F"] == 1) & (df["M"] == 1)]

        return render(request, "rfm.html", {
            "res": df.to_html(index=False),
            "vip": vip.to_html(index=False),
            "welcome": welcome.to_html(index=False),
            "old": old.to_html(index=False),
            "delete": delete.to_html(index=False)
        })


class KmeansView(TemplateView):
    template_name = 'customerAnalysis.html'

    def get(self, request):
        plot_res, name0, name1, name2, email0, email1, email2 = self.handle()
        return render(request, self.template_name, {
            "plot_res": plot_res,
            "name0": name0,
            "name1": name1,
            "name2": name2,
            "email0": email0,
            "email1": email1,
            "email2": email2
        })

    # def post(self, request):
    #    form = CustomerForm(request.POST, request.FILES)
    #    if form.is_valid():
    #        plot_res, mname_list, age_list, consumption_list, kmeans_fit = self.handle_file(request.FILES['file'])
    #        form = CustomerForm()
    #    args = {'form': form, "plot_res": plot_res, "mname_list": mname_list, "age_list": age_list,
    #            "consumption_list": consumption_list, "kmeans_fit": kmeans_fit}
    #    return render(request, self.template_name, args)

    def handle(self):
        memberid_list = []
        mname_list = []
        age_list = []
        consumption_list = []
        email_list = []
        curr = datetime.now()
        for cust in Member.objects.all():
            memberid_list.append(cust.MemberID)
            mname_list.append(cust.mName)
            # Calculate the member's age
            age = (curr.year - cust.BDay.year) - ((curr.month, curr.day) < (cust.BDay.month, cust.BDay.day))
            age_list.append(age)
            # Calculate the member's total consumption amount
            cons = 0
            orders = Order.objects.filter(MID=cust.MemberID)
            for order in orders:
                dish = Dish.objects.filter(dName=order.dishName)
                dish_price = dish[0].dPrice
                cons += dish_price
            consumption_list.append(cons)
            email_list.append(cust.Email)
        df = pd.DataFrame({"id": memberid_list, "name": mname_list, "age": age_list, "consumption": consumption_list,
                           "email": email_list})
        model = KMeans(n_clusters=3)
        kmeans_fit = model.fit_predict(df.iloc[:, 2:4])
        for i in set(kmeans_fit):
            plt.scatter(x=df[(model.labels_ == i)]["age"], y=df[(model.labels_ == i)]["consumption"], label=i)
        plt.legend()
        save_file = BytesIO()
        plt.savefig(save_file, format='png')
        plot_res = base64.b64encode(save_file.getvalue()).decode('utf8')
        plt.close()

        name0 = list(df[(model.labels_ == 0)]["name"])
        name1 = list(df[(model.labels_ == 1)]["name"])
        name2 = list(df[(model.labels_ == 2)]["name"])

        email0 = list(df[(model.labels_ == 0)]["email"])
        email1 = list(df[(model.labels_ == 1)]["email"])
        email2 = list(df[(model.labels_ == 2)]["email"])

        return plot_res, name0, name1, name2, email0, email1, email2


class DecisionTreeView(TemplateView):

    def get(self, request):
        pre = self.decision_tree_calculate()
        return render(request, "decisionTree.html", {
            "pre0": "高" if pre[0] == "High" else "低",
            "pre1": "高" if pre[1] == "High" else "低",
            "pre2": "高" if pre[2] == "High" else "低",
            "pre3": "高" if pre[3] == "High" else "低",
            "pre4": "高" if pre[4] == "High" else "低",
            "pre5": "高" if pre[5] == "High" else "低",
            "pre6": "高" if pre[6] == "High" else "低",
            "pre7": "高" if pre[7] == "High" else "低",
        })

    def decision_tree_calculate(self):
        pets_list = [1 if each.Pets else 0 for each in Member.objects.all()]
        student_list = [1 if each.Student else 0 for each in Member.objects.all()]
        gender_list = [1 if each.Gender == "Male" else 0 for each in Member.objects.all()]
        consumption_list = []
        for cust in Member.objects.all():
            # Calculate the member's total consumption amount
            cons = 0
            orders = Order.objects.filter(MID=cust.MemberID)
            for order in orders:
                dish = Dish.objects.filter(dName=order.dishName)
                dish_price = dish[0].dPrice
                cons += dish_price
            consumption_list.append(cons)
        mean = sum(consumption_list) / len(consumption_list)
        consumption_list = ["High" if each >= mean else "Low" for each in consumption_list]
        df = pd.DataFrame({
            "pets": pets_list,
            "student": student_list,
            "gender": gender_list,
            "consumption": consumption_list
        })
        clf = tree.DecisionTreeClassifier()
        clf = clf.fit(df[["pets", "student", "gender"]], df["consumption"])
        test_df = pd.DataFrame({
            "pets": [0, 0, 0, 0, 1, 1, 1, 1],
            "student": [0, 0, 1, 1, 0, 0, 1, 1],
            "gender": [0, 1, 0, 1, 0, 1, 0, 1]
        })
        pre = clf.predict(test_df)
        return pre


class RetentionRateView(TemplateView):

    def get(self, request):
        curr_time = datetime.now()
        retention_rate_past = self.get_past_retention_rate(curr_time.year, curr_time.month)
        retention_rate_curr = self.get_curr_retention_rate(curr_time.year, curr_time.month)
        return render(request, "retentionRate.html", {
            "retention_past": retention_rate_past,
            "retention_curr": retention_rate_curr
        })

    def get_curr_retention_rate(self, curr_year, curr_month):
        curr_cust = []
        past_cust = []
        for order in Order.objects.all():
            if order.oTime.year == curr_year and order.oTime.month == curr_month:
                curr_cust.append(order.MID)
            elif order.oTime.year == curr_year and order.oTime.month == curr_month - 1:
                past_cust.append(order.MID)
            elif curr_month == 1 and order.oTime.month == 12 and order.oTime.year == (curr_year - 1):
                past_cust.append(order.MID)
        curr_cust = set(curr_cust)
        past_cust = set(past_cust)
        curr_retention = curr_cust & past_cust
        try:
            retention_rate_curr = round(len(curr_retention) / len(past_cust), 2)
        except:
            retention_rate_curr = 0

        return retention_rate_curr

    def get_past_retention_rate(self, curr_year, curr_month):
        past_cust = []
        past_past_cust = []
        for order in Order.objects.all():
            if order.oTime.year == curr_year and order.oTime.month == curr_month - 1:
                past_cust.append(order.MID)
            elif order.oTime.year == curr_year and order.oTime.month == curr_month - 2:
                past_past_cust.append(order.MID)
            elif order.oTime.year == (curr_year - 1) and curr_month == 1 and order.oTime.month == 12:
                past_cust.append(order.MID)
            elif order.oTime.year == (curr_year - 1) and curr_month == 1 and order.oTime.month == 11:
                past_past_cust.append(order.MID)
            elif order.oTime.year == (curr_year - 1) and curr_month == 2 and order.oTime.month == 12:
                past_past_cust.append(order.MID)
        past_cust = set(past_cust)
        past_past_cust = set(past_past_cust)
        past_retention = past_cust & past_past_cust
        try:
            retention_rate_past = round(len(past_retention) / len(past_past_cust), 2)
        except:
            retention_rate_past = 0
        return retention_rate_past


class SurvivalRateView(TemplateView):

    def get(self, request):
        curr_time = datetime.now()
        survival = 1
        survival_list = []
        # 計算存活率
        for year in range(2019, curr_time.year + 1):
            if year != curr_time.year:
                for month in range(1, 13):
                    if year != 2019 or month != 1:
                        retention = RetentionRateView.get_curr_retention_rate(SurvivalRateView, year, month)
                        survival *= retention
                        survival_list.append(round(survival, 2))
            else:
                for month in range(1, curr_time.month + 1):
                    retention = RetentionRateView.get_curr_retention_rate(SurvivalRateView, year, month)
                    survival *= retention
                    survival_list.append(round(survival, 2))

        # 畫圖
        plt.plot(survival_list[-6:])
        plt.legend()
        save_file = BytesIO()
        plt.savefig(save_file, format='png')
        plot_res = base64.b64encode(save_file.getvalue()).decode('utf8')
        plt.close()

        return render(request, 'survivalRate.html', {
            "s1": survival_list[-6],
            "s2": survival_list[-5],
            "s3": survival_list[-4],
            "s4": survival_list[-3],
            "s5": survival_list[-2],
            "s6": survival_list[-1],
            "plot_res": plot_res
        })
