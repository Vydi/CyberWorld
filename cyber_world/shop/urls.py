from django.urls import path
from . import views

urlpatterns = [
    path('', views.MainView.as_view(), name='index'),
    path('products/', views.ProductView.as_view(), name='products'),
    # path('details', views.DetailView.as_view(), name='details'),

]
