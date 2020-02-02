from django.contrib import admin
from .models import Order
# Register your models here.
class OrderAdmin(admin.ModelAdmin):
    list_display=['order_id','status','shipping_total','total']


admin.site.register(Order,OrderAdmin)
