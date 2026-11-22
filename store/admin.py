from django.contrib import admin
from .models import Category,Product,EmailOTP,Address,CartItem,Order,OrderItem,Payment
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
 list_display=('name','category','price','stock','is_active'); list_filter=('category','is_active'); search_fields=('name','description'); prepopulated_fields={'slug':('name',)}
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin): prepopulated_fields={'slug':('name',)}
class OrderItemInline(admin.TabularInline):
 model=OrderItem; extra=0; readonly_fields=('product_name','unit_price','quantity')
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
 list_display=('order_number','user','status','total','created_at'); list_filter=('status','created_at'); search_fields=('order_number','user__username'); inlines=[OrderItemInline]
admin.site.register([EmailOTP,Address,CartItem,Payment])
