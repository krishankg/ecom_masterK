from django.contrib import admin
from .models import ObjectViewedModel,UserSession
#
# class ObjectViewedModelAdmin(admin.ModelAdmin):
#     list_display=['created_on','ip_address','object_id']


admin.site.register(UserSession)
admin.site.register(ObjectViewedModel)
