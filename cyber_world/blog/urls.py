from django.urls import path
from . import views

urlpatterns = [
    path('blog/', views.BlogView.as_view(), name='blog'),
    path('create/', views.CreatePost.as_view(), name='create'),
    path('post/<str:slug>/', views.ViewPosts.as_view(), name='details'),
    path('search/', views.Search.as_view(), name='search'),
    path('author/<str:slug>/', views.Profile_Post.as_view(), name='author'),
    path('post/<str:slug>/update', views.UpdatePost.as_view(), name='post-update'),
    path('post/<str:slug>/delete', views.DeletePost.as_view(), name='post-delete'),
]
