from django.db import models
from .user import User

class CustomerDetails(models.Model):
    customer_name = models.CharField(db_index=True, max_length=50)
    email = models.EmailField(db_index=True, unique=True,max_length=150)
    mobile_number = models.CharField(db_index=True,max_length=10)
    # password = models.CharField(db_index=True,max_length=50,min_length=8)
    address = models.CharField(max_length = 200,null=True)
    city = models.CharField(max_length=150,null=True)
    state= models.CharField(max_length=150,null=True)
    country= models.CharField(max_length=150,null=True)
    pincode= models.CharField(max_length=150,null=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.customer_name
        
    class Meta:
        db_table = 'bliss_customer_details'  