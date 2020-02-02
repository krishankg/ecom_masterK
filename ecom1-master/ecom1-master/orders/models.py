from django.db import models
from ecommerce.utils import unique_order_id_generator
from django.db.models.signals import pre_save,post_save
from billing.models import BillingProfile
from carts.models import Cart
from addresses.models import AddressModel
ORDER_STATUS_CHOICES=(
      ('created','Created'),
      ('paid','Paid'),
      ('shipped','Shipped'),
      ('refunded','Refunded')
)
class OrderManager(models.Manager):
    def new_or_get(self,billing_profile,cart_obj):
        created=False
        qs=self.get_queryset().filter(billing_profile=billing_profile,cart=cart_obj,active=True,status='created')
        if qs.count()==1:
            obj=qs.first()
        else:
            obj=self.model.objects.create(billing_profile=billing_profile,cart=cart_obj)
            created=True
        return obj,created
class Order(models.Model):
    billing_profile=models.ForeignKey(BillingProfile,null=True,on_delete=models.CASCADE,related_name='order_billing_profile')
    order_id=models.CharField(max_length=50,blank=True,null=True)
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE,related_name='order_cart')
    shipping_address=models.ForeignKey(AddressModel,related_name='shipping_address',on_delete=models.CASCADE,null=True,blank=True)
    billing_address=models.ForeignKey(AddressModel,related_name='billing_address',on_delete=models.CASCADE,null=True,blank=True)
    shipping_total=models.DecimalField(default=5.50,decimal_places=2,max_digits=10)
    total=models.DecimalField(default=0,decimal_places=2,max_digits=10)
    status=models.CharField(max_length=50,default='created',choices=ORDER_STATUS_CHOICES)
    active=models.BooleanField(default=True)


    def __str__(self):
        return self.order_id

    objects=OrderManager()

    def update_total(self):
        cart_total=self.cart.total_price
        print("update_total:",cart_total)
        shipping_total=self.shipping_total
        new_total=float(cart_total)+float(shipping_total)
        self.total=new_total
        self.save()
        return new_total

    def check_done(self):
        billing_profile=self.billing_profile
        shipping_address=self.shipping_address
        billing_address=self.billing_address
        total=self.total
        if billing_profile and shipping_address and billing_address and total > 0:
            return True
        return False

    def mark_done(self):
        if self.check_done():
            self.status="paid"
            self.save()
        return self.status


def pre_save_order_id(sender,instance,*args,**kwargs):
    if not instance.order_id:
        instance.order_id=unique_order_id_generator(instance)
    qs=Order.objects.filter(cart=instance.cart).exclude(billing_profile=instance.billing_profile)
    if qs.exists():
        qs.update(active=False)

pre_save.connect(pre_save_order_id,sender=Order)


def post_save_total(sender,instance,created,*args,**kwargs):
    if not created:
        cart_obj=instance
        cart_id=cart_obj.id
        cart_total=cart_obj.total_price
        qs=Order.objects.filter(cart__id=cart_id)
        if qs.count()==1:
            order_obj=qs.first()
            order_obj.update_total()


post_save.connect(post_save_total,sender=Cart)

def post_save_order(sender,instance,created,*args,**kwargs):
    print("running----")
    if created:
        print("updated...")
        instance.update_total( )


post_save.connect(post_save_order,sender=Order)
