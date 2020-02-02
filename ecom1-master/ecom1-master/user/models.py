from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager,PermissionsMixin
from ecommerce.utils import random_string_generator,unique_key_generator
from django.db.models.signals import pre_save,post_save
from django.core.mail import send_mail
from django.urls import reverse_lazy,reverse
from django.template.loader import get_template
from django.utils import timezone
from datetime import timedelta
# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self,email,fullname,phone,password=None,staff=True,admin=True,is_active=True):
        if not email:
            raise ValueError("User must have an email adddress.")
        if not password:
            raise ValueError("User mush have an password .")
        if not fullname:
            raise ValueError("User must have a full name.")
        if not phone:
            raise ValueError("User must have a phone number.")

        user_obj=self.model(email=self.normalize_email(email),fullname=fullname,phone=phone)
        user_obj.staff=staff
        user_obj.admin=admin
        user_obj.is_active=is_active
        user_obj.set_password(password)
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self,email,fullname,phone,password=None):
        user=self.create_user(email,fullname,phone,password=password,staff=True)
        return user


    def create_superuser(self,email,fullname,phone,password=None):
        user=self.create_user(email,fullname,phone,password=password,staff=True,admin=True)
        return user
class UserModel(AbstractBaseUser):
    email=models.EmailField(max_length=200,unique=True)
    fullname=models.CharField(max_length=30)
    phone=models.CharField(max_length=11)
    is_active=models.BooleanField(default=True)
    staff=models.BooleanField(default=False)
    admin=models.BooleanField(default=False)
    timestamp=models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['fullname','phone']
    objects=UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.fullname

    def get_short_name(self):
        return self.fullname

    def has_perm(self,perm,obj=None):
        return True

    def has_module_perms(self,app_label):
        return True

    @property
    def is_admin(self):
        return self.admin
    @property
    def is_staff(self):
        return self.staff
    # @property
    # def is_active(self):
    #     return self.active

DEFAULT_ACTIVATION_DAYS=getattr(settings,'DEFAULT_ACTIVATION_DAYS')
class EmailActivationQuerySet(models.query.QuerySet):
    def confirm(self):
        now=timezone.now()
        start_range=now-timedelta(days=DEFAULT_ACTIVATION_DAYS)
        end_range=now
        return self.filter(
             activated=False,
             force_expired=False
             ).filter(
              created_on__gt=start_range,
              created_on__lte=end_range,
               )

class EmailActivationManager(models.Manager):
    def get_queryset(self):
        return EmailActivationQuerySet(self.model,using=self._db)

class EmailActivation(models.Model):
    user=models.ForeignKey(UserModel,on_delete=models.CASCADE)
    email=models.EmailField()
    key=models.CharField(max_length=120,blank=True,null=True)
    activated=models.BooleanField(default=False)
    force_expired=models.BooleanField(default=False)
    expired=models.IntegerField(default=7)
    updated_on=models.DateTimeField(auto_now=True)
    created_on=models.DateTimeField(auto_now_add=True)

    objects=EmailActivationManager()

    def can_activate(self):
        qs=EmailActivation.objects.filter(pk=self.pk)
        if qs.exists():
            return True
        return False

    def activate(self):
        if self.can_activate():
            user=self.user
            user.is_active=True
            user.save()
            self.activated=True
            self.save()
            return True
        return False



    def __str__(self):
        return self.email

    def regenerate(self):
        self.key=None
        self.save()
        if self.key is not None:
            return True
        else:
            return False

    def send_activation_email(self):
        if not self.activated and not self.force_expired:
            if self.key:
                base_url=getattr(settings,'BASE_URL')
                key_path=reverse("users:activate_email",kwargs={'key':self.key})
                path="{base}{path}".format(base=base_url,path=key_path)
                context={
                 'path':path,
                 'email':self.email,
                 'user':self.user.fullname
                }
                txt_=get_template("registration/email_activation/email_verfication.txt").render(context)
                html_=get_template("email/email_confirmation_message.html").render(context)
                subject='Email Verification'
                from_email=settings.DEFAULT_EMAIL_HOST
                recipient_list=[self.email]
                sent_mail=send_mail(
                      subject,
                      txt_,
                      from_email,
                      recipient_list,
                      html_message=html_,
                      fail_silently=False,
                     )
                return sent_mail
        return False


def pre_save_email_verification(sender,instance,*args,**kwargs):
    if not instance.activated and not instance.force_expired:
        if not instance.key:
            instance.key=unique_key_generator(instance)


pre_save.connect(pre_save_email_verification,sender=EmailActivation)

def post_save_user_create_receiver(sender,instance,created,*args,**kwargs):
    if created:
        obj=EmailActivation.objects.create(user=instance,email=instance.email)
        obj.send_activation_email()

post_save.connect(post_save_user_create_receiver,sender=UserModel)
