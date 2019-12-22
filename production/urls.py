from django.urls import path
import production.views

urlpatterns = [
    path('',production.views.main),
]