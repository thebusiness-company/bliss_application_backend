from django.db import models
from .customer_details import CustomerDetails
from .product import Product
from .user import User
class Cart(models.Model):
    customer = models.ForeignKey(CustomerDetails,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    product_qty = models.IntegerField()
    created_by = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=50)  #check it
    class Meta:
        db_table = 'bliss_cart_details'  
       