from django.shortcuts import render, redirect
from .models import Product, ProductCategory, Customer
from tiendapp.models import OrderDetail, Order
from django.contrib import messages

# Create your views here.

def v_index(request):
    products_db = Product.objects.all()
    
    context = {
        "products": products_db
    }
    return render(request, "tiendapp/index.html", context)


def v_cart(request):
    customer_obj = Customer.objects.get(user = request.user)
    
    order_current = customer_obj.get_current_order()
    # order_current tipo: Order
    details = OrderDetail.objects.filter(order = order_current)
    
    context = {
        "items": details
    }
    return render(request, "tiendapp/cart.html", context)


def v_product_detail(request, code):
    product_obj = Product.objects.get(sku = code)

    rels = ProductCategory.objects.filter(product = product_obj)

    # rels_ids, guarda los ids categoria del producto
    rels_ids = [rr.category.id for rr in rels]
    sug = ProductCategory.objects.filter(
        category__in = rels_ids).exclude(product = product_obj)
    # sug, posee a las sugerencias, pero necesito los ids de los productos
    sug_ids = [ss.product.id for ss in sug]
    extras = Product.objects.filter(id__in = sug_ids)

    context = {
        "product": product_obj,
        "extras": extras
    }

    return render(request, "tiendapp/product_detail.html", context)

def v_add_to_cart(request, code):
    if not request.user.is_authenticated:
        return redirect("sign_in")
    print(f"Código SKU recibido: {repr(code)}")
    product_obj = Product.objects.get(sku = code)
    # request.user, guarda variables de sesión
    customer_obj = Customer.objects.get(user = request.user)
    
    order_current = customer_obj.get_current_order()
    
    # Verifica que exista un producto seleccionado previamente
    detail_obj = OrderDetail.objects.filter(product = product_obj, order = order_current).first()
    
    if detail_obj is not None: # Actualizar price
        detail_obj.price = product_obj.price
        detail_obj.save()
    else: # Crear item en carro
        detail_obj = OrderDetail()
        detail_obj.product = product_obj
        detail_obj.order = order_current    
        detail_obj.quantity = 1
        detail_obj.price = product_obj.price
        detail_obj.save()
    return redirect("/cart")

def v_remove_from_cart(request, code):
    # Eliminar del carrito
    product_obj = Product.objects.get(sku = code)
    
    customer_obj = Customer.objects.get(user = request.user)
    
    current_order = customer_obj.get_current_order()
    
    item_cart = OrderDetail.objects.filter(order = current_order, product = product_obj).first()
    
    if item_cart is not None:
        item_cart.delete()
        
    return redirect("/cart")    

def v_checkout(request):
    customer = Customer.objects.get(user = request.user)
    current_order = customer.get_current_order()
    details = OrderDetail.objects.filter(order = current_order)
    
    total = 0 #=> entero
    # item => OrderDetail
    for item in details:
        subtotal = item.price * item.quantity
        total = total + subtotal
    
    context = {
        "items": details,
        "total_order": total,
        "customer": customer
    }
    
    return render(request, "tiendapp/checkout.html", context )

def v_checkout_end(request):
    # Validar si request.method es Post
    if request.method == "POST":
        customer_obj = Customer.objects.get(user = request.user)
        
        # Capturar a la orden en cro del cliente en la variable: current_order
        current_order = customer_obj.get_current_order()
        
        data = request.POST.copy()
        
        current_order.shipping_address = data["shipping_address"]
        current_order.status = "PAGADO"
        
        current_order.save()
        
        messages.success(request, "La orden se ha procesado correctamente")
        
        return redirect("/")
