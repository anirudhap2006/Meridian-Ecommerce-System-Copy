from decimal import Decimal
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Category,Product,Address,CartItem,Order,Payment
class MeridianFlowTests(TestCase):
 def setUp(self):
  self.user=User.objects.create_user(username='customer',password='StrongPass123!',email='customer@example.com')
  c=Category.objects.create(name='Books',slug='books')
  self.product=Product.objects.create(category=c,name='Python Basics',slug='python-basics',description='Intro book',price=Decimal('499.00'),stock=5)
  self.address=Address.objects.create(user=self.user,full_name='Test Customer',phone='9999999999',line1='12 Test Road',city='Bengaluru',state='Karnataka',postal_code='560001')
 def test_catalog_search(self):
  self.assertContains(self.client.get(reverse('home'),{'q':'Python'}),'Python Basics')
 def test_cart_requires_login(self):
  self.assertEqual(self.client.get(reverse('cart')).status_code,302)
 def test_add_to_cart(self):
  self.client.login(username='customer',password='StrongPass123!')
  self.client.post(reverse('add_to_cart',args=[self.product.pk]),{'quantity':2})
  self.assertEqual(CartItem.objects.get(user=self.user).quantity,2)
 def test_successful_checkout(self):
  self.client.login(username='customer',password='StrongPass123!')
  CartItem.objects.create(user=self.user,product=self.product,quantity=2)
  s=self.client.session; s['checkout_address']=self.address.pk; s.save()
  self.client.post(reverse('payment'),{'method':'DEMO_UPI','outcome':'success'})
  self.product.refresh_from_db(); order=Order.objects.get(user=self.user)
  self.assertEqual(order.status,'PLACED'); self.assertEqual(self.product.stock,3)
  self.assertEqual(Payment.objects.get(order=order).status,'SUCCESS')
 def test_failed_payment_preserves_stock(self):
  self.client.login(username='customer',password='StrongPass123!')
  CartItem.objects.create(user=self.user,product=self.product,quantity=1)
  s=self.client.session; s['checkout_address']=self.address.pk; s.save()
  self.client.post(reverse('payment'),{'method':'DEMO_CARD','outcome':'failure'})
  self.product.refresh_from_db()
  self.assertEqual(self.product.stock,5); self.assertEqual(Order.objects.get(user=self.user).status,'CANCELLED')
