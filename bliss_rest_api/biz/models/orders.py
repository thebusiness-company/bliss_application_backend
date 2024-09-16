
from django.db import models
from .customer_details import CustomerDetails
from .product import Product


class Order(models.Model):
    customer = models.ForeignKey(CustomerDetails, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length =10,null=True)
    quantity = models.CharField(max_length =10,null=False)
    email = models.EmailField(max_length=150, null=False)
    phone = models.CharField(max_length=20, null=False)
    address = models.TextField(null=False)
    city = models.CharField(max_length=150, null=False)
    state= models.CharField(max_length=150, null=False)
    country= models.CharField(max_length=150, null=False)
    pincode= models.CharField(max_length=150, null=False)
    total_price = models.FloatField(null=True)
    payment_mode=models.CharField(max_length=150,null=False)
    payment_id=models.CharField(max_length=250, null=True)
    status=models.CharField(max_length=150,default='Pending')
    # message=models.TextField(null=True)
    tracking_no=models.CharField(max_length=250, null=True)
    created_by = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=50)

    def __str__(self):
        return '{} - {}'.format(self.id,self.customer_id,self.tracking_no)

    class Meta:
        db_table = 'bliss_order_details'     