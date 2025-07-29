from django.shortcuts import render
from django.views.generic import TemplateView
from django.views import View
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms
from django.shortcuts import render, redirect

# Create your views here.

class HomePageView(TemplateView):
    template_name="pages/home.html"

class AboutPageView(TemplateView):
    template_name="pages/about.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "title":"About us - Online Store",
            "subtitle":"About us",
            "description":"This is an about page ...",
            "author":"Developed by: Samuel Ariza"
        })
        return context
    
class ContactPageView(TemplateView):
    template_name="pages/contact.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "title":"Contact - Online Store",
            "subtitle":"Contact",
        })
        return context

class Product:
    products = [
        {"id":"1", "name":"TV", "description":"Best TV", "price": 499.99},
        {"id":"2", "name":"iPhone", "description":"Best iPhone", "price": 999.99},
        {"id":"3", "name":"Chromecast", "description":"Best Chromecast", "price": 49.99},
        {"id":"4", "name":"Glasses", "description":"Best Glasses", "price": 99.99}
    ]

class ProductIndexView(View):
    template_name = 'products/index.html'

    def get(self, request):
        viewData = {}
        viewData["title"] = "Products - Online Store"
        viewData["subtitle"] = "List of products"
        viewData["products"] = Product.products

        return render(request, self.template_name, viewData)

class ProductShowView(View):
    template_name = 'products/show.html'

    def get(self, request, id):
        try:
            product = Product.products[int(id)-1]
            viewData = {}
            viewData["title"] = product["name"] + " - Online Store"
            viewData["subtitle"] = product["name"] + " - Product information"
            viewData["product"] = product
            return render(request, self.template_name, viewData)
        except (IndexError, ValueError):
            return HttpResponseRedirect(reverse('home'))
        
class ProductForm(forms.Form):
    name = forms.CharField(required=True)
    price = forms.FloatField(required=True)

    def clean_price(self):
        price = self.cleaned_data['price']
        if price <= 0:
            raise forms.ValidationError("Price must be greater than 0.")
        return price

class ProductCreateView(View):
    template_name = 'products/create.html'

    def get(self, request):
        form = ProductForm()
        viewData = {}
        viewData["title"] = "Create product"
        viewData["form"] = form
        return render(request, self.template_name, viewData)

    def post(self, request):
        form = ProductForm(request.POST)
        if form.is_valid():
            new_id = str(len(Product.products) + 1)
            Product.products.append({
                "id": new_id,
                "name": form.cleaned_data["name"],
                "description": "New product",
                "price": form.cleaned_data["price"]
            })
            viewData = {}
            viewData["title"] = "Product Created"
            viewData["message"] = "Product created"
            return render(request, 'products/success.html', viewData)
        else:
            viewData = {}
            viewData["title"] = "Create product"
            viewData["form"] = form
            return render(request, self.template_name, viewData)