from django.db import models
from django.conf import settings
from django.db.models.signals import pre_save,post_save

User=settings.AUTH_USER_MODEL
class BillingProfileManager(models.Manager):
    def new_or_get(self,request):
        obj=None
        created=None
        print("request:",request)
        if request.user.is_authenticated:
            obj,created=self.model.objects.get_or_create(user=request.user,email=request.user.email)
        return obj,created

    
class BillingProfile(models.Model):
    user       =models.OneToOneField(User,on_delete=models.CASCADE,unique=True,null=True,blank=True)
    email      =models.EmailField()
    active     =models.BooleanField(default=True)
    updated_on =models.DateTimeField(auto_now=True)
    created_on =models.DateTimeField(auto_now_add=True)
    objects=BillingProfileManager()

    def __str__(self):
        return self.email



def post_save_profile(sender,instance,created,*args,**kwargs):
    if created and instance.email:
        BillingProfile.objects.get_or_create(user=instance,email=instance.email)

post_save.connect(post_save_profile,sender=User)
