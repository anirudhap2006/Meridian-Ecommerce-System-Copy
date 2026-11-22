import random
from datetime import timedelta
from decimal import Decimal
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db import transaction
from django.db.models import Q,F
from django.shortcuts import render,redirect,get_object_or_404
from django.utils import timezone
from django.views.decorators.http import require_POST
from .forms import RegisterForm,AddressForm
from .models import Category,Product,EmailOTP,CartItem,Address,Order,OrderItem,Payment

def home(request):
 products=Product.objects.filter(is_active=True,stock__gt=0).select_related('category')
 q=request.GET.get('q','').strip(); cat=request.GET.get('category',''); sort=request.GET.get('sort','newest')
 if q: products=products.filter(Q(name__icontains=q)|Q(description__icontains=q)|Q(category__name__icontains=q))
 if cat: products=products.filter(category__slug=cat)
 products=products.order_by('price' if sort=='price_low' else '-price' if sort=='price_high' else '-created_at')
 return render(request,'store/home.html',{'products':products,'categories':Category.objects.all(),'q':q,'selected_category':cat,'sort':sort})
def product_detail(request,slug):
 return render(request,'store/product_detail.html',{'product':get_object_or_404(Product,slug=slug,is_active=True)})
def register(request):
 if request.method=='POST':
  form=RegisterForm(request.POST)
  if form.is_valid():
   data={k:form.cleaned_data[k] for k in ('username','email','password')}
   code=f'{random.randint(0,999999):06d}'
   EmailOTP.objects.filter(email=data['email']).delete()
   EmailOTP.objects.create(email=data['email'],code=code,payload=data,expires_at=timezone.now()+timedelta(minutes=10))
   send_mail('Meridian email verification code',f'Your Meridian verification code is {code}. It expires in 10 minutes.',settings.DEFAULT_FROM_EMAIL,[data['email']])
   request.session['pending_email']=data['email']; messages.info(request,'Verification code sent. In development, check the VS Code terminal.')
   return redirect('verify_email')
 else: form=RegisterForm()
 return render(request,'store/register.html',{'form':form})
def verify_email(request):
 email=request.session.get('pending_email')
 if not email: return redirect('register')
 if request.method=='POST':
  otp=EmailOTP.objects.filter(email=email).order_by('-created_at').first()
  code=request.POST.get('code','').strip()
  if otp and otp.is_valid(code):
   data=otp.payload; user=User.objects.create_user(username=data['username'],email=data['email'],password=data['password'])
   otp.delete(); request.session.pop('pending_email',None); login(request,user)
   messages.success(request,'Email verified. Welcome to Meridian!'); return redirect('home')
  messages.error(request,'Invalid or expired verification code.')
 return render(request,'store/verify_email.html',{'email':email})
@login_required
def add_to_cart(request,product_id):
 product=get_object_or_404(Product,pk=product_id,is_active=True)
 if request.method=='POST':
  try: qty=max(1,int(request.POST.get('quantity',1)))
  except ValueError: qty=1
  if qty>product.stock: messages.error(request,'Requested quantity is not available.')
  else:
   item,created=CartItem.objects.get_or_create(user=request.user,product=product,defaults={'quantity':qty})
   if not created: item.quantity=min(product.stock,item.quantity+qty); item.save()
   messages.success(request,'Added to your cart.')
 return redirect('cart')
@login_required
def cart(request):
 items=request.user.cart_items.select_related('product','product__category')
 subtotal=sum((i.subtotal for i in items),Decimal('0.00'))
 return render(request,'store/cart.html',{'items':items,'subtotal':subtotal})
@login_required
@require_POST
def update_cart(request,item_id):
 item=get_object_or_404(CartItem,pk=item_id,user=request.user); action=request.POST.get('action')
 if action=='remove': item.delete()
 else:
  try: qty=int(request.POST.get('quantity',1))
  except ValueError: qty=1
  if qty<1: item.delete()
  elif qty<=item.product.stock: item.quantity=qty; item.save()
  else: messages.error(request,'Quantity exceeds available stock.')
 return redirect('cart')
@login_required
def addresses(request):
 form=AddressForm(request.POST or None)
 if request.method=='POST' and form.is_valid():
  a=form.save(commit=False); a.user=request.user; a.save(); messages.success(request,'Address saved.'); return redirect('checkout')
 return render(request,'store/addresses.html',{'form':form,'addresses':request.user.addresses.all()})
@login_required
def checkout(request):
 items=list(request.user.cart_items.select_related('product'))
 if not items: messages.info(request,'Your cart is empty.'); return redirect('home')
 addresses=request.user.addresses.all()
 if request.method=='POST':
  a=get_object_or_404(Address,pk=request.POST.get('address'),user=request.user); request.session['checkout_address']=a.pk; return redirect('payment')
 subtotal=sum((i.subtotal for i in items),Decimal('0.00'))
 return render(request,'store/checkout.html',{'items':items,'addresses':addresses,'subtotal':subtotal,'total':subtotal})
@login_required
def payment(request):
 aid=request.session.get('checkout_address'); address=get_object_or_404(Address,pk=aid,user=request.user) if aid else None
 items=list(request.user.cart_items.select_related('product'))
 if not address or not items: return redirect('checkout')
 total=sum((i.subtotal for i in items),Decimal('0.00'))
 if request.method=='POST':
  method=request.POST.get('method','DEMO_CARD'); outcome=request.POST.get('outcome','success')
  if method not in ('DEMO_CARD','DEMO_UPI'): method='DEMO_CARD'
  with transaction.atomic():
   locked=list(CartItem.objects.select_for_update().filter(user=request.user).select_related('product'))
   for item in locked:
    if item.quantity>item.product.stock: messages.error(request,f'Insufficient stock for {item.product.name}.'); return redirect('cart')
   order=Order.objects.create(user=request.user,address=address,subtotal=total,total=total)
   for item in locked:
    OrderItem.objects.create(order=order,product=item.product,product_name=item.product.name,unit_price=item.product.price,quantity=item.quantity)
    if outcome=='success': Product.objects.filter(pk=item.product_id).update(stock=F('stock')-item.quantity)
   status='SUCCESS' if outcome=='success' else 'FAILED'
   Payment.objects.create(order=order,transaction_id='MRDTX'+str(random.randint(100000000,999999999)),method=method,status=status,amount=total)
   if outcome=='success':
    CartItem.objects.filter(user=request.user).delete(); request.session.pop('checkout_address',None)
    messages.success(request,'Demo payment successful. Order placed.'); return redirect('order_detail',order_number=order.order_number)
   order.status='CANCELLED'; order.save(update_fields=['status'])
   messages.error(request,'Demo payment failed. Order cancelled; stock was not deducted.'); return redirect('orders')
 return render(request,'store/payment.html',{'address':address,'items':items,'total':total})
@login_required
def orders(request):
 return render(request,'store/orders.html',{'orders':request.user.orders.order_by('-created_at')})
@login_required
def order_detail(request,order_number):
 order=get_object_or_404(Order.objects.prefetch_related('items','payments'),order_number=order_number,user=request.user)
 return render(request,'store/order_detail.html',{'order':order})
@login_required
@require_POST
def cancel_order(request,order_number):
 with transaction.atomic():
  order=get_object_or_404(Order.objects.select_for_update(),order_number=order_number,user=request.user)
  if order.status in ('PLACED','CONFIRMED'):
   for item in order.items.all(): Product.objects.filter(pk=item.product_id).update(stock=F('stock')+item.quantity)
   order.status='CANCELLED'; order.save(update_fields=['status']); order.payments.filter(status='SUCCESS').update(status='REFUNDED')
   messages.success(request,'Order cancelled. Demo refund recorded.')
  else: messages.error(request,'This order can no longer be cancelled.')
 return redirect('order_detail',order_number=order_number)
