from django.db import models
from .customer_details import CustomerDetails
from .product import Product
from .orders import Order
from django.db.models.fields import CharField
from django.utils.translation import gettext_lazy as _
from biz.constants import PaymentStatus

class RazorpayPayment(models.Model):
    # name = models.CharField(_("CustomerName"), max_length=254, blank=False, null=False)
    customername = models.CharField(max_length=254, blank=False, null=False)
    amount = models.FloatField(null=False, blank=False)
    paymentstatus = models.CharField(
        default=PaymentStatus.PENDING,
        max_length=254,
        blank=False,
        null=False,
    )
    provider_order_id = models.CharField( max_length=40, null=False, blank=False
    )
    payment_id = models.CharField(max_length=36, null=False, blank=False
    )
    signature_id = models.CharField(max_length=128, null=False, blank=False
    )

    def __str__(self):
        return f"{self.id}-{self.name}-{self.status}"    