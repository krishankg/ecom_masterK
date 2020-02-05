from django.contrib import admin
from .models import UserProfile
class UserProfileAdmin(admin.ModelAdmin):
    list_display =('user','date_of_birth','photo','gender',)
    list_filter =('user','date_of_birth')
    search_fields=('date_of_birth',)

admin.site.register(UserProfile,UserProfileAdmin)
