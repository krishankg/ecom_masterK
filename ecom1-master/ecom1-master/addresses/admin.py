from django.contrib import admin
from .models import AddressModel
# Register your models here.

class AddressModelAdmin(admin.ModelAdmin):
    list_display=['address_line_1','address_line_2','country','state','city','postal_code']




admin.site.register(AddressModel,AddressModelAdmin)
