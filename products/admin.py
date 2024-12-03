from django.contrib import admin
from .models import Product, ProductImage

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','price','stock','is_active','created_at')
    prepopulated_fields = {'slug':('name',)}

class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product',"image")

admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage, ProductImageAdmin)