from django.urls import path
import production.views

urlpatterns = [
    path('orderSystem/', production.views.orderSystem),
    path('checkSystem/', production.views.checkSystem),
    path('provideSystem/', production.views.provideSystem),
    path('stockCheck/', production.views.stockCheck),
    path('equipmentCheck/', production.views.equipmentCheck),
    path('stockProvide/', production.views.stockProvide),
    path('equipmentProvide/', production.views.equipmentProvide),
]
