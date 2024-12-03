from django.db import models

# Create your models here.
class Payment(models.Model):
    STATUS_CHOICES = [
        ('PENDING','Pending'),
        ("COMPLETED",'completed'),
        ('FAILED','Failed'),
    ]
    transaction_id = models.CharField(max_length=100,unique=True,blank=True,null=True)
    phone_number = models.CharField(max_length=15)
    amount = models.DecimalField(max_digits=10,decimal_places=2)
    payment_time = models.DateTimeField(blank=True, null=True)
    customer_name = models.CharField(max_length=100,blank=True,null=True)
    verified = models.BooleanField(default=False)
    status = models.CharField(max_length=10,choices=STATUS_CHOICES,default='PENDING')

    def __str__(self):
        return f"{self.customer_name or 'unknown'} - {self.amount} ({self.status})"
