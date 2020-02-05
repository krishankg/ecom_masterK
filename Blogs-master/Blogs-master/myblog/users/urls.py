from django.urls import path
from .views import home

urlpatterns=[
         path('login/',home,name='login'),
]
