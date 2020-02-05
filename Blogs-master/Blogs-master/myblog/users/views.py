from django.shortcuts import render
from .models import UserProfile
from django.views.generic import TemplateView
def home(TemplateView):
    template_name='users/home.html'
