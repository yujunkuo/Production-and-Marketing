from django.urls import path
import production.views

urlpatterns = [
    path('orderSystem/', production.views.orderSystem),
    path('inventorySystem/', production.views.inventorySystem),
    path('equipmentSystem/', production.views.equipmentSystem),
]
