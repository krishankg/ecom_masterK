from django.shortcuts import render
from django.views.generic import ListView,DetailView
from .models import Product
from django.http import Http404
from carts.models import Cart
from django.db.models import Q
from user_info.mixins import ObjectViewedMixins
class ProductListView(ListView):
    model=Product
    template_name='products/product_list.html'
    context_object_name='objects'
    def get_queryset(self,*args,**kwargs):
        request=self.request
        queryset=Product.objects.all()
        return queryset
    def get_context_data(self,*args,**kwargs):
        context=super(ProductListView,self).get_context_data(*args,**kwargs)
        context['name']='Krishn Kumar Patel'
        return context


class ProductDetailView(DetailView):
    model=Product
    template_name='products/product_detail.html'
    context_object_name='object'

    def get_context_data(self,*args,**kwargs):
        context=super(ProductDetailView,self).get_context_data(*args,**kwargs)
        cart_obj,new_obj=Cart.objects.new_or_get(self.request)
        context['cart']=cart_obj
        return context
    def get_object(self,*args,**kwargs):
        request=self.request
        slug=self.kwargs.get('slug')
        print("slug:",slug)
        try:
            instance=Product.objects.get(slug=slug)
        except Product.DoesNotExist:
            raise Http404("Product Does't exists .")
        except Product.MultipleObjectReturned:
            qs=Product.objects.filter(slug=slug)
            instance=qs.first()
        except:
            raise Http404('Not Found.')
        # object_viewed_signal(instance.__class__,instance=instance,request=request)
        return instance
