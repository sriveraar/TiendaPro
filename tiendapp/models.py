from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    sku = models.CharField(max_length=64)
    name = models.CharField(max_length=256)
    price = models.DecimalField(decimal_places=2, max_digits=6)
    weight = models.DecimalField(decimal_places=2, max_digits=6)
    description = models.TextField()
    thumbnail = models.ImageField(upload_to="products/")
    image = models.ImageField(upload_to="products_image/")
    create_date = models.DateField()
    stock = models.DecimalField(decimal_places=2, max_digits=6)
    
    def __str__(self):
        return self.name
    
class Category(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()
    
    def __str__(self):
        return self.name
    
class ProductCategory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    
    def __str__(self):
        return self.category.name + " > " + self.product.name
    
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    billing_address = models.TextField()
    shipping_address = models.TextField()
    phone = models.CharField(max_length=64)
    
    def __str__(self):
        return self.user.username + " Teléfono:" + self.phone

class Order(models.Model):
    # CUSTOMER tiene muchas ORDERS
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    shipping_address = models.TextField()
    order_date = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=32) #Pendiente #Pagadp
    
    def __str__(self):
        return self.customer.user.username + " Estado Order:" + self.status
    
class OrderDetail(models.Model):
    # RDER tiene muchos ORDER DETAIL
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    # PRODUCT tiene muchas ORDER DETAIL
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    price = models.DecimalField(decimal_places=2, max_digits=6) #9999.12
    quantity = models.DecimalField(decimal_places=2, max_digits=6) #9999.12
    
    def __str__(self):
        return str(self.order.id) + " " + self.product.name
