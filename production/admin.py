from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Member)
admin.site.register(Dish)
admin.site.register(Stock)
admin.site.register(Equipment)
admin.site.register(Firm)
admin.site.register(Order)
admin.site.register(Made)
admin.site.register(ProvideEquip)
admin.site.register(ProvideStock)


