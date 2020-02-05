from django.shortcuts import render, get_object_or_404
from .models import Post
from django.views.generic import ListView,DetailView
from django.core.paginator import Paginator

class PostListView(ListView):
    model=Post
    template_name='blog/list.html'
    context_object_name='objects'

class PostDetailView(DetailView):
    model=Post
    template_name='blog/post.html'
    context_object_name='object'
