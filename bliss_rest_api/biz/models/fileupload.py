from django.db import models


class FileUpload(models.Model):
    tmp_file_name = models.CharField(max_length=150)
    orig_file_name = models.CharField(max_length=100)
    storage_file_name = models.CharField(max_length=150, null=True)
    source_field = models.CharField(max_length=100, null=True)

    uploaded_by = models.CharField(max_length=60)
    is_moved = models.BooleanField(null=True)
    moved_at = models.DateTimeField(null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "bliss_file_upload"