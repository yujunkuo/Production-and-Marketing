from django.shortcuts import render
from django.views.generic import TemplateView
from .forms import CustomerForm

import pandas as pd
from sklearn.cluster import KMeans
# Create your views here.

def main(request):
    return render(request, 'main.html')

def members(request):
    return render(request, 'members.html')

class CustomerView(TemplateView):

    template_name = 'customerAnalysis.html'

    def get(self, request):
        form = CustomerForm()
        return render(request, self.template_name, {
            "form": form
        })

    def post(self, request):
        form = CustomerForm(request.POST, request.FILES)
        if form.is_valid():
            output = self.handle_file(request.FILES['file'])
            form = CustomerForm()
        args = {'form': form, 'output': output}
        return render(request, self.template_name, args)

    def handle_file(self, file):
        df = pd.read_csv(file)
        kmeans_fit = KMeans(n_clusters=3).fit_predict(df.iloc[1:,1:])
        return kmeans_fit
