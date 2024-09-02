from django.db import models
from django.contrib.postgres.fields import ArrayField
class Product(models.Model):
    # category=models.ForeignKey(Category,on_delete=models.CASCADE)
    product_name=models.CharField(max_length=150)
    # product_image = models.JSONField(default=list, blank=True)
    product_image = ArrayField(models.CharField(max_length=255), blank=True, default=list)
    
    # product_image=models.CharField(max_length=150)
    quantity=models.IntegerField()
    original_price=models.FloatField()
    selling_price=models.FloatField()
    description=models.TextField(max_length=150)
    status = models.BooleanField(default=False)
    trending=models.BooleanField(default=False)
    availability=models.BooleanField(default=True)
    created_by = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=50)

    def __str__(self):
        return self.product_name

    class Meta:
        db_table = 'bliss_product_details'    
        