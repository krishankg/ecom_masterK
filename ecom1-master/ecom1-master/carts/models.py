from django.db import models
from django.conf import settings
from products.models import Product
from django.db.models.signals import pre_save,post_save,m2m_changed
User=settings.AUTH_USER_MODEL

class CartManager(models.Manager):
    def new(self,user=None):
        user_obj=None
        if user is not None:
             if user.is_authenticated:
                user_obj=user
        return self.model.objects.create(user=user_obj)

    def new_or_get(self,request):
        cart_id=request.session.get('cart_id',None)
        qs=self.get_queryset().filter(id=cart_id)
        if qs.count()==1:
            new_obj=False
            cart_obj=qs.first()
            if request.user.is_authenticated and cart_obj.user is None:
                cart_obj.user=request.user
                cart_obj.save()
        else:
            cart_obj=Cart.objects.new(user=request.user)
            new_obj=True
            request.session['cart_id']=cart_obj.id
        return cart_obj,new_obj



class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    products=models.ManyToManyField(Product,blank=True)
    subtotal=models.DecimalField(default=0,decimal_places=2,max_digits=10)
    total_count=models.PositiveIntegerField(default=0,blank=True,null=True)
    total_price=models.DecimalField(default=0,decimal_places=2,max_digits=10)
    update_on=models.DateTimeField(auto_now=True)
    timestamp=models.DateTimeField(auto_now_add=True)
    quantity=models.PositiveIntegerField(default=1)
    objects=CartManager()

    def __str__(self):
        return str(self.id)


def pre_save_cart(sender,instance,action,*args,**kwargs):
    if action== 'post_add' or action =='post_remove' or action=='post_clear':
        products=instance.products.all()
        print(products)
        count=0
        total=0
        for product in products:
            total=total+product.price
            count=count+1
        instance.subtotal=total
        instance.total_count=count
        instance.save()
m2m_changed.connect(pre_save_cart,sender=Cart.products.through)

def pre_save_cart_add(sender,instance,*args,**kwargs):
    if instance.subtotal>0:
        instance.total_price=instance.subtotal+40
    else:
        instance.total_price=0.00

pre_save.connect(pre_save_cart_add,sender=Cart)
