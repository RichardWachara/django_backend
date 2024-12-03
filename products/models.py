from django.db import models

# Create your models here.

class Product(models.Model):
    
    name = models.CharField(max_length=255, unique=True, help_text="Name of the product")
    slug = models.SlugField(unique=True,help_text="Unique_slug for the product")
    description = models.TextField(blank=True,help_text="Detailed description of the product")

    # Pricing of the product
    price = models.DecimalField(max_digits=10, decimal_places=2,help_text="Price of the product")
    discount_price = models.DecimalField(max_digits=10, decimal_places=2,help_text="Discount price of the product")

    # Inventory of the product - is it in stock and is it available for purchase
    stock = models.PositiveIntegerField(default=0,help_text="Number of items available")
    is_active= models.BooleanField(default=True,help_text="Whether the product is available for purchase")

    # The images of the product
    image = models.ImageField(upload_to='products/images/',blank=True,null=True,help_text="The main image of the product")
    additional_images= models.ManyToManyField('ProductImage', blank=True,related_name='products_with_images', help_text="Additional product images")

    # TimeStamp
    created_at = models.DateTimeField(auto_now_add=True,help_text="Timestamp when the product was created")
    updated_at = models.DateTimeField(auto_now_add=True,help_text="Timestamp when the product was last updated")

    def __str__(self):
        return self.name
    
    @property
    def is_on_sale(self):
        return self.discount_price is not None and self.discount_price < self.price
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Products"
        verbose_name_plural = "Products"

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="additional_product_images")
    image = models.ImageField(upload_to='products/additional_images/')
    alt_text = models.CharField(max_length=255,blank=True,help_text="Alternative text for the image")

    def __str__(self):
        return f'Image for {self.product.name}'
