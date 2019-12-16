from django.conf.urls import url
from marketing.views import CustomerView
urlpatterns = [
  url(r'^$', CustomerView.as_view(), name="customer")
]