import secrets
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.crypto import get_random_string
class Category(models.Model):
 name=models.CharField(max_length=80,unique=True); slug=models.SlugField(unique=True)
 def __str__(self): return self.name
class Product(models.Model):
 category=models.ForeignKey(Category,on_delete=models.PROTECT,related_name='products')
 name=models.CharField(max_length=180); slug=models.SlugField(unique=True); description=models.TextField()
 price=models.DecimalField(max_digits=10,decimal_places=2); stock=models.PositiveIntegerField(default=0)
 image_url=models.URLField(blank=True); is_active=models.BooleanField(default=True); created_at=models.DateTimeField(auto_now_add=True)
 def __str__(self): return self.name
class EmailOTP(models.Model):
 email=models.EmailField(db_index=True); code=models.CharField(max_length=6); payload=models.JSONField()
 expires_at=models.DateTimeField(); created_at=models.DateTimeField(auto_now_add=True)
 def is_valid(self, code): return self.code==code and self.expires_at>=timezone.now()
class Address(models.Model):
 user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='addresses')
 full_name=models.CharField(max_length=120); phone=models.CharField(max_length=20); line1=models.CharField(max_length=200)
 line2=models.CharField(max_length=200,blank=True); city=models.CharField(max_length=80); state=models.CharField(max_length=80)
 postal_code=models.CharField(max_length=12); is_default=models.BooleanField(default=False)
 def __str__(self): return f'{self.full_name} - {self.city}'
class CartItem(models.Model):
 user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='cart_items')
 product=models.ForeignKey(Product,on_delete=models.CASCADE); quantity=models.PositiveIntegerField(default=1)
 class Meta: unique_together=('user','product')
 @property
 def subtotal(self): return self.product.price*self.quantity
class Order(models.Model):
 STATUS_CHOICES=[('PLACED','Placed'),('CONFIRMED','Confirmed'),('SHIPPED','Shipped'),('DELIVERED','Delivered'),('CANCELLED','Cancelled')]
 user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT,related_name='orders')
 address=models.ForeignKey(Address,on_delete=models.PROTECT)
 order_number=models.CharField(max_length=16,unique=True,blank=True)
 status=models.CharField(max_length=12,choices=STATUS_CHOICES,default='PLACED')
 subtotal=models.DecimalField(max_digits=10,decimal_places=2,default=0); shipping_fee=models.DecimalField(max_digits=8,decimal_places=2,default=0)
 total=models.DecimalField(max_digits=10,decimal_places=2,default=0); created_at=models.DateTimeField(auto_now_add=True)
 def save(self,*args,**kwargs):
  if not self.order_number: self.order_number='MRD'+get_random_string(9,allowed_chars='ABCDEFGHJKLMNPQRSTUVWXYZ23456789')
  super().save(*args,**kwargs)
 def __str__(self): return self.order_number
class OrderItem(models.Model):
 order=models.ForeignKey(Order,on_delete=models.CASCADE,related_name='items'); product=models.ForeignKey(Product,on_delete=models.PROTECT)
 product_name=models.CharField(max_length=180); unit_price=models.DecimalField(max_digits=10,decimal_places=2); quantity=models.PositiveIntegerField()
 @property
 def line_total(self): return self.unit_price*self.quantity
class Payment(models.Model):
 STATUS_CHOICES=[('SUCCESS','Success'),('FAILED','Failed'),('REFUNDED','Refunded')]
 METHOD_CHOICES=[('DEMO_CARD','Demo card'),('DEMO_UPI','Demo UPI')]
 order=models.ForeignKey(Order,on_delete=models.CASCADE,related_name='payments')
 transaction_id=models.CharField(max_length=24,unique=True); method=models.CharField(max_length=12,choices=METHOD_CHOICES)
 status=models.CharField(max_length=10,choices=STATUS_CHOICES); amount=models.DecimalField(max_digits=10,decimal_places=2)
 created_at=models.DateTimeField(auto_now_add=True)
