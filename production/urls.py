from django.urls import path
import production.views

urlpatterns = [
    path('memeberJoin/', production.views.JoinMemberView.as_view()),
    path('orderSystem/', production.views.OrderView.as_view()),
    path('stockCheck/', production.views.CheckStockAllView.as_view()),
    path('stockCheck/', production.views.CheckStockNeedView.as_view()),
    path('stockCheck/', production.views.CheckStockExpiredView.as_view()),
    path('equipmentCheck/', production.views.CheckEquipAllView.as_view()),
    path('equipmentCheck/', production.views.CheckEquipNeedView.as_view()),
    path('stockProvide/', production.views.ProvideStockView.as_view()),
    path('equipmentProvide/', production.views.ProvideEquipView.as_view()),
    path('prediction/', production.views.prediction),
]
