from django.shortcuts import render
from .models import Product

# Create your views here.

def v_index(request):
    products_db = Product.objects.all()
    
    context = {
        "products": products_db
    }
    return render(request, "tiendapp/index.html", context)


def v_cart(request):
    context = {
        "items": [None, None, None, None]
    }
    return render(request, "tiendapp/cart.html", context)


def v_product_detail(request, code):
    product_obj = Product.objects.get(sku = code)
    
    context = {
        "product": product_obj
    }        
    return render(request, "tiendapp/product_detail.html", context)
