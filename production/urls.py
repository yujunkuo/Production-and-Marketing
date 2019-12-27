from django.urls import path
import production.views

urlpatterns = [
    path('memeberJoin/', production.views.JoinMemberView.as_view()),
    path('orderSystem/', production.views.OrderView.as_view()),
    path('stockCheck/', production.views.CheckStockView.as_view()),
    path('equipmentCheck/', production.views.equipmentCheck),
    path('stockProvide/', production.views.stockProvide),
    path('equipmentProvide/', production.views.equipmentProvide),
]
