from django.db import models

class CollectionQuery(models.Model):
    key = models.CharField(max_length=50, unique=True)
    query = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.key
    
    class Meta:
        db_table = 'bliss_collection_query'