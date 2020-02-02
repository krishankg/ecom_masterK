from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from .signals import object_viewed_signal
from .utils import get_client_ip_address
from django.contrib.sessions.models  import Session
from django.db.models.signals import pre_save,post_save
from user.signals import user_logged_in
from user.models import UserModel
User=settings.AUTH_USER_MODEL
from django.contrib.auth.models import AnonymousUser


FORCE_SESSION_TO_ONE=getattr(settings,'FORCE_SESSION_TO_ONE',False)
FORCE_INACTIVE_USER_ENDSESSION=getattr(settings,'FORCE_INACTIVE_USER_ENDSESSION',False)


class ObjectViewedModel(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    ip_address=models.CharField(max_length=50,blank=True,null=True)
    content_type=models.ForeignKey(ContentType,on_delete=models.CASCADE)
    object_id=models.PositiveIntegerField()
    content_object=GenericForeignKey('content_type','object_id')
    created_on=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} viewed on {}".format(self.content_object,self.created_on)


    class Meta:
        ordering=['-created_on']
        verbose_name='Object viewed'
        verbose_name_plural='objects viewed'


def object_viewed_receiver(sender,instance,request,*args,**kwargs):
    content_type_model=ContentType.objects.get_for_model(sender)  # instance.__class__
    new_object_viewed=ObjectViewedModel.objects.create(
                 content_type=content_type_model,
                 object_id=instance.id,
                 ip_address=get_client_ip_address(request),
                 )
    if request.user:
        new_object_viewed.user=request.user
        new_object_viewed.save()
    else:
        user=AnonymousUser()
        new_object_viewed.user=user
        new_object_viewed.save()


object_viewed_signal.connect(object_viewed_receiver)



class UserSession(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    ip_address=models.CharField(max_length=50,blank=True,null=True)
    session_key=models.CharField(max_length=100,blank=True,null=True)
    active=models.BooleanField(default=True)
    ended=models.BooleanField(default=False)
    created_on=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user.fullname)


    def end_session(self):
        session_key=self.session_key
        ended=self.ended
        try:
            Session.objects.get(pk=session_key).delete()
            self.active=False
            self.ended=True
            self.save()
        except:
            pass

        return self.ended

def post_save_session(sender,instance,created,*args,**kwargs):
    if created:
        qs=UserSession.objects.filter(user=instance.user,ended=False,active=False).exclude(id=instance.id)
        for i in qs:
            i.end_session()
    if not instance.active and not instance.ended:
        instance.end_session()

def post_save_changed_session(sender,instance,created,*args,**kwargs):
    if created:
        if instance.is_active==False:
            qs=UserSession.objects.filter(user=instance.user,ended=False,active=False).exclude(id=instance.id)
            for i in qs:
                i.end_session()

if FORCE_SESSION_TO_ONE:
    post_save.connect(post_save_session,sender=UserSession)


if FORCE_INACTIVE_USER_ENDSESSION:
    post_save.connect(post_save_changed_session,sender=UserModel)



def user_logged_in_receiver(sender,instance,request,*args,**kwargs):
    print(instance)
    user=instance
    session_key=request.session.session_key
    ip_address=get_client_ip_address(request)

    new_session_obj=UserSession.objects.create(
          user=user,
          ip_address=ip_address,
          session_key=session_key
          )


user_logged_in.connect(user_logged_in_receiver)
