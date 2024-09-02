from django.db import models

class Role(models.Model): 
    name = models.CharField(max_length=50)
    display_value = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    code = models.CharField(max_length=10, db_index=True, unique=True)
    role_cat = models.CharField(max_length=30, null=True, blank=True)
    created_by = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'biz_role'
        