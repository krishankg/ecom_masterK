from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from addresses.views import checkout_address_create_view
from django.conf.urls.static import static
from carts.views import cart_detail_update_view
from payments.views import checkout_payment
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('products.urls',namespace='products')),
    path('search/',include('search.urls',namespace='searchs')),
    path('tag/',include('tag.urls',namespace='tags')),
    path('carts/',include('carts.urls',namespace='carts')),
    path('api/cart/',cart_detail_update_view,name="cart_api"),
    path('user/',include('user.urls',namespace='users')),
    path('orders/',include('orders.urls',namespace='orders')),
    path('checkout/address/create/',checkout_address_create_view,name='checkout_address_create'),
    path('accounts/',include('user.password.urls')),
    path('payments/',checkout_payment,name='payments'),


]
if settings.DEBUG:
    urlpatterns=urlpatterns+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns=urlpatterns+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
