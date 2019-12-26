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


# Create your views here.

def main(request):
    return render(request, 'main.html')


def members(request):
    return render(request, 'members.html')


def swot(request):
    return render(request, 'swot.html')


def stp(request):
    return render(request, 'stp.html')


class KmeansView(TemplateView):
    template_name = 'customerAnalysis.html'

    def get(self, request):
        # form = CustomerForm()
        plot_res, mname_list, age_list, consumption_list, kmeans_fit = self.handle_file()
        return render(request, self.template_name, {
            "plot_res": plot_res,
            "mname_list": mname_list,
            "age_list": age_list,
            "consumption_list": consumption_list,
            "kmeans_result": kmeans_fit
        })

    # def post(self, request):
    #    form = CustomerForm(request.POST, request.FILES)
    #    if form.is_valid():
    #        plot_res, mname_list, age_list, consumption_list, kmeans_fit = self.handle_file(request.FILES['file'])
    #        form = CustomerForm()
    #    args = {'form': form, "plot_res": plot_res, "mname_list": mname_list, "age_list": age_list,
    #            "consumption_list": consumption_list, "kmeans_fit": kmeans_fit}
    #    return render(request, self.template_name, args)

    def handle_file(self):
        memberid_list = []
        mname_list = []
        age_list = []
        consumption_list = []
        curr = datetime.now()
        for cust in Member.objects.all():
            memberid_list.append(cust.MemberID)
            mname_list.append(cust.mName)
            # Calculate the member's age
            age = (curr.year - cust.BDay.year) - ((curr.month, curr.day) < (cust.BDay.month, cust.BDay.day))
            age_list.append(age)
            # Calculate the member's total consumption amount
            cons = 0
            orders = Order.objects.filter(MemberID=cust.MemberID)
            for order in orders:
                dish = Dish.objects.filter(dName=order.dName)
                dish_price = dish[0].dPrice
                cons += dish_price
            consumption_list.append(cons)
        df = pd.DataFrame({"id": memberid_list, "name": mname_list, "age": age_list, "consumption": consumption_list})
        model = KMeans(n_clusters=3)
        kmeans_fit = model.fit_predict(df.iloc[:, 2:])
        for i in set(kmeans_fit):
            plt.scatter(x=df[(model.labels_ == i)]["age"], y=df[(model.labels_ == i)]["consumption"], label=i)
        plt.legend()
        save_file = BytesIO()
        plt.savefig(save_file, format='png')
        plot_res = base64.b64encode(save_file.getvalue()).decode('utf8')
        plt.close()
        return plot_res, mname_list, age_list, consumption_list, kmeans_fit


class DecisionTreeView(TemplateView):

    def get(self, request):
        pets_list = [1 if each.Pets else 0 for each in Member.objects.all()]
        student_list = [1 if each.Student else 0 for each in Member.objects.all()]
        gender_list = [1 if each.Gender == "Male" else 0 for each in Member.objects.all()]
        consumption_list = []
        for cust in Member.objects.all():
            # Calculate the member's total consumption amount
            cons = 0
            orders = Order.objects.filter(MemberID=cust.MemberID)
            for order in orders:
                dish = Dish.objects.filter(dName=order.dName)
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
        return render(request, "decisionTree.html", {
            "pre0": pre[0],
            "pre1": pre[1],
            "pre2": pre[2],
            "pre3": pre[3],
            "pre4": pre[4],
            "pre5": pre[5],
            "pre6": pre[6],
            "pre7": pre[7]
        })


class RetentionRateView(TemplateView):

    def get(request):
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
                curr_cust.append(order.MemberID)
            elif order.oTime.year == curr_year and order.oTime.month == curr_month - 1:
                past_cust.append(order.MemberID)
            elif curr_month == 1 and order.oTime.month == 12 and order.oTime.year == (curr_year - 1):
                past_cust.append(order.MemberID)
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
                past_cust.append(order.MemberID)
            elif order.oTime.year == curr_year and order.oTime.month == curr_month - 2:
                past_past_cust.append(order.MemberID)
            elif order.oTime.year == (curr_year - 1) and curr_month == 1 and order.oTime.month == 12:
                past_cust.append(order.MemberID)
            elif order.oTime.year == (curr_year - 1) and curr_month == 1 and order.oTime.month == 11:
                past_past_cust.append(order.MemberID)
            elif order.oTime.year == (curr_year - 1) and curr_month == 2 and order.oTime.month == 12:
                past_past_cust.append(order.MemberID)
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
        for year in range(2019, curr_time.year + 1):
            if year != curr_time.year:
                for month in range(1, 13):
                    retention = RetentionRateView.get_curr_retention_rate(SurvivalRateView, year, month)
                    survival *= retention
                    if curr_time.month < 6 and year == (curr_time.year - 1) and month >= (7 + curr_time.month):
                        survival_list.append(survival)
            else:
                for month in range(1, curr_time.month + 1):
                    retention = RetentionRateView.get_curr_retention_rate(SurvivalRateView, year, month)
                    survival *= retention
                    if curr_time.month > 6 and month >= 13 - curr_time.month:
                        survival_list.append(survival)
        return render(request, 'survivalRate.html', {
            "s1": survival_list[0],
            "s2": survival_list[1],
            "s3": survival_list[2],
            "s4": survival_list[3],
            "s5": survival_list[4],
            "s6": survival_list[5]
        })
