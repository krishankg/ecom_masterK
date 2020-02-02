from django.contrib import admin
from .models import BillingProfile

class BillingProfileAdmin(admin.ModelAdmin):
    list_display=['email','created_on','updated_on']




admin.site.register(BillingProfile,BillingProfileAdmin)
