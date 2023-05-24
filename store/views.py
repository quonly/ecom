from django.shortcuts import render
from .models import *
from django.db.models import Sum,F
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
import json
from datetime import datetime
from .utils import cookieCart, cartData, guestOrder
# Create your views here.

def store(request):
  data = cookieCart(request)
  cartItems = data['cartItems']
      
  products = Product.objects.all()
  context = {
    'products':products,
    'cartItems':cartItems,
  }
  return render(request,'store/store.html',context)

def cart(request):
  data = cookieCart(request)
  cartItems = data['cartItems']
  order = data['order']
  items = data['items']

    
  context = {
    'items':items,
    'order':order,
    'cartItems':cartItems,
  }
  return render(request,'store/cart.html',context)

def checkout(request):
  data = cookieCart(request)
  cartItems = data['cartItems']
  order = data['order']
  items = data['items']
    
  context = {
    'items':items,
    'order':order,
    'cartItems':cartItems,
    'checkout':True,
  }
  return render(request,'store/checkout.html',context)

# we just want return some kind of message, we dont want template
def updateItem(request):
  data = json.loads(request.body)
  print(data)
  productId = data['productId']
  action = data['action']
  print(productId,action)
  
  customer = request.user.customer
  product = Product.objects.get(id=productId)
  order, created = Order.objects.get_or_create(customer=customer,complete=False)

  orderItem, created = OrderItem.objects.get_or_create(order=order,product=product)
  
  if action == 'add':
    orderItem.quantity = (orderItem.quantity + 1)
  elif action == 'remove':
    orderItem.quantity = (orderItem.quantity - 1 )
    
  orderItem.save()
  quantity = orderItem.quantity
  total_price_item = "{:,.2f}".format(orderItem.get_total)
  cart_total = "{:,.2f}".format(order.get_cart_total)
  cartItems = order.get_cart_items
  if orderItem.quantity <=0:
    orderItem.delete()
  
  return JsonResponse({
    'totalPriceItem':total_price_item,
    'quantity':quantity,
    'cartTotal':cart_total,
    'cartItems': cartItems
    }) # safe=False ทำให้รีเทิร์น value ที่ไม่ใช่ dict ได้
  
def processOrder(request):
  transaction_id = datetime.now().timestamp()
  data = json.loads(request.body)
  if request.user.is_authenticated:
    customer = request.user.customer
    order, created = Order.objects.get_or_create(customer=customer,complete=False)
    total = float(data['form']['total'])
    order.transaction_id = transaction_id
    
    if total == order.get_cart_total:
      order.complete = True
    order.save()
    
    if order.shipping == True:
      ShippingAddress.objects.create(
        customer=customer,
        order=order,
        address=data['shipping']['address'],
        city=data['shipping']['state'],
        zipcode = data['shipping']['zipcode']
      )
  else:
    customer, order = guestOrder(request, data)
  total = float(data['form']['total'])
  order.transaction_id = transaction_id
  
  if total == order.get_cart_total:
    order.complete = True
  order.save()

  if order.shipping == True:
    ShippingAddress.objects.create(
      customer=customer,
      order=order,
      address=data['shipping']['address'],
      city=data['shipping']['state'],
      zipcode = data['shipping']['zipcode']
    )  
    
  return JsonResponse('Payment complete',safe=False)