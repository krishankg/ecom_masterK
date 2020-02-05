from django.urls import path,include
from .views import PostListView,PostDetailView

urlpatterns=[
        path('list/',PostListView.as_view(),name='list'),
        path('details/<slug:slug>/',PostDetailView.as_view(),name='details'),
]
