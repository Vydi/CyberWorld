from django.shortcuts import render
from django.views.generic import TemplateView


# Create your views here.

class MainView(TemplateView):
    template_name = "index.html"


# class DetailView(TemplateView):
#     template_name = "details.html"

class ProductView(TemplateView):
    template_name = "product.html"


