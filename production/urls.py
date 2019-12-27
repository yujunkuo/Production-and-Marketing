from django.urls import path
import production.views

urlpatterns = [
    path('orderSystem/', production.views.OrderView.as_view()),
    path('memberJoin/'), production.views.memeberJoin),
    path('stockCheck/', production.views.stockCheck),
    path('equipmentCheck/', production.views.equipmentCheck),
    path('stockProvide/', production.views.stockProvide),
    path('equipmentProvide/', production.views.equipmentProvide),
]
