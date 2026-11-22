from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
urlpatterns=[
 path('',views.home,name='home'),path('products/<slug:slug>/',views.product_detail,name='product_detail'),
 path('register/',views.register,name='register'),path('verify-email/',views.verify_email,name='verify_email'),
 path('login/',auth_views.LoginView.as_view(template_name='store/login.html'),name='login'),
 path('logout/',auth_views.LogoutView.as_view(),name='logout'),path('cart/',views.cart,name='cart'),
 path('cart/add/<int:product_id>/',views.add_to_cart,name='add_to_cart'),
 path('cart/update/<int:item_id>/',views.update_cart,name='update_cart'),path('addresses/',views.addresses,name='addresses'),
 path('checkout/',views.checkout,name='checkout'),path('payment/',views.payment,name='payment'),
 path('orders/',views.orders,name='orders'),path('orders/<str:order_number>/',views.order_detail,name='order_detail'),
 path('orders/<str:order_number>/cancel/',views.cancel_order,name='cancel_order')]
