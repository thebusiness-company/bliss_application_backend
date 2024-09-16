from django.db import models

class ContactSubmission(models.Model): 
    name = models.CharField(max_length=50,null=False)
    email = models.EmailField(db_index=True,max_length=150,null=True)
    mobile_number = models.CharField(db_index=True,max_length=10,null=True)
    message=models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'bliss_contact_submission'