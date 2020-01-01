from django.urls import path
import production.views

urlpatterns = [
    path('memeberJoin/', production.views.JoinMemberView.as_view()),
    path('orderSystem/', production.views.OrderView.as_view()),
    path('stockCheck/', production.views.CheckStockView.as_view()),
    path('equipmentCheck/', production.views.CheckEquipView.as_view()),
    path('stockProvide/', production.views.ProvideStockView.as_view()),
    path('equipmentProvide/', production.views.ProvideEquipView.as_view()),
    path('prediction/', production.views.predictionView.as_view()),
]
