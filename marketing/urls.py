from django.urls import path
from marketing.views import KmeansView, swot

urlpatterns = [
  path('cluster/kmeans/', KmeansView.as_view()),
  path('swot/', swot),
]