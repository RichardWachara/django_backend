from django.contrib import admin
from .models import Payment

# Register your models here.
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('transaction_id','customer_name','phone_number','status','verified')


admin.site.register(Payment,PaymentAdmin)