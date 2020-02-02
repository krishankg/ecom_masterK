from django.contrib import admin
from .models import Cart

class CartAdmin(admin.ModelAdmin):
    list_display=['total_count','timestamp','update_on','total_price']



admin.site.register(Cart,CartAdmin)
