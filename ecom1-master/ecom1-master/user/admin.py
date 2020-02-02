from django.contrib import admin
from .models import UserModel
# Register your models here.
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from .forms import UserAdminCreationForm,UserAdminChangeForm
from user.models import EmailActivation

class UserAdmin(BaseUserAdmin):
    form=UserAdminChangeForm
    add_form=UserAdminCreationForm

    list_display=['email','admin','fullname','phone']
    list_filter=('admin',)
    fieldsets=(
       (None,{'fields':('email','phone','password')}),
       ('Personal info',{'fields':('fullname',)}),
       ('Permissions',{'fields':('admin','staff','is_active')}),
    )

    add_fieldsets=(
    (None,{
       'classes':('wide',),
       'fields':('email','password1','password2')}
       ),
    )

    search_fields=('email','fullname',)
    ordering=('email',)
    filter_horizontal=()

#
# class UserModelAdmin(admin.ModelAdmin):
#     list_display=['email','fullname','phone']
#     search_fields=('email','fullname',)
#     form=UserAdminChangeForm
#     add_form=UserAdminCreationForm
#
#     class Meta:
#         model=UserModel

class EmailActivationAdmin(admin.ModelAdmin):
    list_display=['email','key']


admin.site.register(UserModel,UserAdmin)
admin.site.unregister(Group)
admin.site.register(EmailActivation,EmailActivationAdmin)
