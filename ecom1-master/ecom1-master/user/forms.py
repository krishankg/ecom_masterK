from django import forms
from user.models import UserModel
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth import authenticate,login,logout
from user.signals import user_logged_in

class UserAdminCreationForm(forms.ModelForm):
    password1=forms.CharField(label='Password',widget=forms.PasswordInput)
    password2=forms.CharField(label='Confirm Password',widget=forms.PasswordInput)

    class Meta:
        model=UserModel
        fields=('email','fullname','phone','is_active','password')

    def clean_password2(self):
        password1=self.cleaned_data.get('password1')
        password2=self.cleaned_data.get('password2')
        if password1 and password2 and password1 !=password2:
            raise forms.ValidationError("Password don't match.")
        return password2

    def save(self,commit=True):
        user=super(UserAdminCreationForm,self).save(commit=False)
        user.set_password(self.cleaned_data.get('password1'))
        if commit:
            user.save()
        return user

class UserAdminChangeForm(forms.ModelForm):
    password=ReadOnlyPasswordHashField()
    class Meta:
        model=UserModel
        fields=('email','fullname','phone','password','is_active','admin')
    def clean_password(self):
        return self.initial['password']


# login form
class LoginForm(forms.Form):
    email=forms.CharField(max_length=50)
    password=forms.CharField(widget=forms.PasswordInput())

    def __init__(self,request,*args,**kwargs):
        self.request=request
        super(LoginForm,self).__init__(*args,**kwargs)

    def clean(self):
        data=self.cleaned_data
        email=data.get('email')
        password=data.get('password')
        user=authenticate(self.request,username=email,password=password)
        if user is None:
            raise forms.ValidationError('Invalid Credentials,Please Try again')
        login(self.request,user)
        user_logged_in.send(user,instance=user,request=self.request)
        self.user=user
        return data

    def clean_email(self):
        email=self.cleaned_data.get('email')
        if not UserModel.objects.filter(email=email).exists():
            raise forms.ValidationError("Please Enter Valid email.")
        else:
            return email


#Registrations forms

class RegistrationForm(forms.ModelForm):
    password1=forms.CharField(label='Password',widget=forms.PasswordInput)
    password2=forms.CharField(label='Confirm Password',widget=forms.PasswordInput)

    class Meta:
        model=UserModel
        fields=('email','fullname','phone')

    def clean_email(self):
        email=self.cleaned_data.get('email')
        if UserModel.objects.filter(email=email).exists():
            raise forms.ValidationError("This email have been already taken.")
        return email

    def clean_password2(self):
        password1=self.cleaned_data.get('password1')
        password2=self.cleaned_data.get('password2')
        if password1 and password2 and password1 !=password2:
            raise forms.ValidationError("Password don't match.")
        return password2

    def save(self,commit=True):
        user=super(RegistrationForm,self).save(commit=False)
        user.set_password(self.cleaned_data.get('password1'))
        user.is_active=False # form confirmation
        if commit:
            user.save()
        return user


class UserDetailChangeForm(forms.ModelForm):
    fullname=forms.CharField(label='Name',max_length=35,required=False)
    phone=forms.CharField(label='Mobile No.',max_length=11,required=False)
    class Meta:
        model=UserModel
        fields=['fullname','phone']
