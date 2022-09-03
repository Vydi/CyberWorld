from django.urls import path
from . import views

urlpatterns = [
    path('blog', views.BlogView.as_view(), name='blog'),
    path('create/', views.CreatePost.as_view(), name='create'),
    path('post/<str:slug>/', views.ViewPosts.as_view(), name='details'),
    path('search/', views.Search.as_view(), name='search'),
]
