from django.urls import path
import production.views

urlpatterns = [
    path('memeberJoin/', production.views.JoinMemberView.as_view()),
    path('orderSystem/', production.views.OrderView.as_view()),
    path('stockCheck/', production.views.stockCheck),
    path('equipmentCheck/', production.views.equipmentCheck),
    path('stockProvide/', production.views.ProvideStockView.as_view()),
    path('equipmentProvide/', production.views.ProvideEquipView.as_view()),
    path('prediction/', production.views.prediction),
]
