from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf.urls import url
app_name='user'

urlpatterns=[
     path('account/',views.AccountHomeView.as_view(),name='account_home'),
     path('details/',views.AccountUpdateView.as_view(),name='user-update'),
     path('login/',views.LoginView.as_view(),name='login'),
     path('logout/',views.Logout,name='logout'),
     path('signup/',views.Registration.as_view(),name='signup'),
     url(r'email/activate/confirm/(?P<key>[0-9a-zA-Z]+)/',views.AccountEmailActivationView.as_view(),name='activate_email'),
     path('email/activate/mailsend-your-email-address/',views.email_send,name='email_send'),
]
