from django.shortcuts import render,redirect
from products.models import Product
from django.http import JsonResponse
from .models import Cart
from orders.models import Order
from addresses.models import AddressModel
from billing.models import BillingProfile
from django.contrib.auth.decorators import login_required
from addresses.forms import AddressForm
from django.http import HttpResponse
from carts.models import Cart


def cart_detail_update_view(request):
    cart_obj,new_obj=Cart.objects.new_or_get(request)
    product_obj=cart_obj.objects.all()
    products=[{"name":x.name,"price":x.price} for x in product_obj]
    cart_data={'products':products,"subtotal":cart_obj.subtotal,"total":cart_obj.total}
    return JsonResponse(cart_data)
def cart_home(request):
    cart_obj,new_obj=Cart.objects.new_or_get(request)
    return render(request,'carts/home.html',{"cart":cart_obj})

def cart_update(request):
    product_id=request.POST.get('product_id')
    print("product_id:",product_id)
    if product_id is not None:
         try:
             product_obj=Product.objects.get(id=product_id)
         except Product.DoesNotExist:
             return HttpResponse('some thing worong.')
         cart_obj,new_obj=Cart.objects.new_or_get(request)
         if product_obj in cart_obj.products.all():
              cart_obj.products.remove(product_obj)
              added=False
         else:
              cart_obj.products.add(product_obj)
              added=True
         request.session['cart_items']=cart_obj.products.count()
         if request.is_ajax():
             json_data={"added":added,"removed":not added,"cartItemCounts":cart_obj.products.count()}
             return JsonResponse(json_data)
    return redirect('carts:cart')

def checkout_home(request):

  if request.user.is_authenticated:
    cart_obj,cart_created=Cart.objects.new_or_get(request)
    order_obj=None
    if cart_created or cart_obj.products.count()==0:
      return redirect("carts:cart")
    user=request.user
    billing_address_id = request.session.get("billing_address_id", None)
    shipping_address_id = request.session.get("shipping_address_id", None)
    print("billing_address_id:",billing_address_id)
    print("shipping_address_id:",shipping_address_id)
    address_qs=None
    billing_profile=None
    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    if billing_profile is not None:
      if user.is_authenticated:
        address_qs = AddressModel.objects.filter(billing_profile=billing_profile)
        order_obj, order_obj_created = Order.objects.new_or_get(billing_profile, cart_obj)
        if shipping_address_id:
          order_obj.shipping_address = AddressModel.objects.get(id=shipping_address_id)
        if billing_address_id:
          order_obj.billing_address = AddressModel.objects.get(id=billing_address_id) 
        if billing_address_id or shipping_address_id:
          order_obj.save()
    if request.method=="POST":
      is_done=order_obj.check_done()
      if is_done:
        order_obj.mark_done()
        del request.session['cart_id']
        return render(request,'carts/order_success.html')
    address_form=AddressForm()
    products=None
    cart=Cart.objects.filter(user=request.user).select_related('user')
    if cart.count()==1:
      print("count",cart.count())
      cart=cart.first()
      product=cart.products
    context={'products':product,'object':order_obj,'billing_profile':billing_profile,'address_form':address_form}
    return render(request,"carts/checkout.html",context)
  else:
    return redirect('users:login')
