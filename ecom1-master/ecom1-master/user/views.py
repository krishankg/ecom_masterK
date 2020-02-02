from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login,authenticate,logout
from django.views.generic import CreateView,View,TemplateView,DetailView
from .forms import LoginForm
from django.contrib.messages.views import  SuccessMessageMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.http import is_safe_url
from user.forms import RegistrationForm
from django.views.generic import FormView, RedirectView,CreateView,DetailView,View,UpdateView
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from user.models import UserModel
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import EmailActivation
from django.urls import reverse,reverse_lazy
from django.utils.safestring import mark_safe
from .forms import UserDetailChangeForm
from .signals import user_logged_in


class AccountUpdateView(UpdateView):
    form_class=UserDetailChangeForm
    template_name='user/editdetail.html'

    def get_object(self):
        return self.request.user

    def get_context_data(self,*args,**kwargs):
        context=super(AccountUpdateView,self).get_context_data(*args,**kwargs)
        context['title']='Change your Profile Here'
        return context
class AccountHomeView(LoginRequiredMixin,DetailView):
    template_name='user/home.html'
    model=UserModel
    def get_object(self):
        return self.request.user

class AccountEmailActivationView(View):
    def get(self,request,key,*args,**kwargs):
        qs=EmailActivation.objects.filter(key__iexact=key).confirm()
        if qs.count()==1:
            qs=qs.first()
            qs.activate()
            messages.success(request,'Your account is activated Successfully,You can login now!')
            return redirect('users:login')
        else:
            activated_qs=qs.filter(key__iexact=key,activated=True)
            if activated_qs.exists():
                reset_link=reverse('password_reset')
                msg="""Your email have been alreay activated,Do you need to <a href="{link}">reset your reset password</a>.""".format(link=reset_link)
                messages.success(request,mark_safe(msg))
                return redirect('users:login')
        return render(request,'registration/activation_error.html',{})
class Registration(CreateView):
    form_class=RegistrationForm
    template_name='user/registration.html'
    success_url=reverse_lazy('user:email_send')

def email_send(request):
    return render(request,'email/mailsend.html')
# class LoginView(SuccessMessageMixin,FormView):
#     success_url = 'products:list'
#     form_class = LoginForm
#     template_name = 'user/login.html'
#     redirect_field_name = REDIRECT_FIELD_NAME
#     def get(self,*args,**kwargs):
#         form=LoginForm()
#         return render(self.request,'user/login.html',{'form':form})
#
#     def post(self,*args,**kwargs):
#         next_=self.request.GET.get('next')
#         next_post=self.request.POST.get('next')
#         redirect_path=next_ or next_post
#         form=LoginForm(self.request.POST)
#         if form.is_valid():
#             email=form.cleaned_data.get('email')
#             password=form.cleaned_data.get('password')
#             user=authenticate(self.request,email=email,password=password)
#             if user is not None:
#                 auth_login(self.request,user)
#                 self.request.session['id']=user.id
#                 # self.request.session.set_expiry(300)
#
#                 # messages.success(self.request,"you have logged in successfully....")
#                 if is_safe_url(redirect_path,self.request.get_host()):
#                     return redirect(redirect_path)
#                 else:
#                     return redirect('products:list')
#
#             else:
#                 messages.error(self.request,'Sorry Invalid Creditional....')
#                 return redirect('users:login')
#         return render(self.request,'user/registration.html',{'form':form})

def Logout(request):
    auth_logout(request)
    return redirect('user:login')



class LoginView(FormView):
    form_class=LoginForm
    template_name='user/login.html'

    def get_form_kwargs(self):
        kwargs=super(LoginView,self).get_form_kwargs()
        kwargs['request']=self.request
        return kwargs

    def get_next_url(self):
        request=self.request
        next_=request.GET.get('next')
        next_post=request.POST.get('next')
        redirect_path=next_ or next_post or None
        if is_safe_url(redirect_path,request.get_host()):
            return redirect_path
        return "/"

    def form_valid(self,form):
        user=form.user
        if user.is_authenticated:
            next_path=self.get_next_url()
            return redirect(next_path)
        return super(LoginView,self).form_invalid(form)
