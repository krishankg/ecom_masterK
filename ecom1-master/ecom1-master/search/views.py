from django.shortcuts import render
from django.views.generic import ListView
from django.http import Http404
from products.models import Product
from django.db.models import Q
class SearchProductListView(ListView):
    model=Product
    template_name='search/search_list.html'
    context_object_name='objects'
    def get_queryset(self,*args,**kwargs):
        request=self.request
        query=request.GET.get('q')
        if query:
            lookups=(Q(name__icontains=query)|
            Q(descripation__icontains=query))
            return Product.objects.filter(lookups).distinct()
        else:
            return Product.objects.none()
    def get_context_data(self,*args,**kwargs):
        context=super(SearchProductListView,self).get_context_data(*args,**kwargs)
        context['queryset']=Product.objects.all()
        return context
