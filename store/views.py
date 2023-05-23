from django.shortcuts import render
from .models import *
from django.db.models import Sum,F

# Create your views here.
def store(request):
  products = Product.objects.all()
  context = {
    'products':products
  }
  return render(request,'store/store.html',context)

def cart(request):
  # if request.user.is_authenticated:
  #   customer = request.user.customer
  #   # order = Order.objects.get(customer=customer,complete=False)
  #   order, created = Order.objects.get_or_create(customer=customer,complete=False)
  #   # items = OrderItem.objects.filter(order=order)
  #   # query child  by setting the parent value and then the child object with all lowercase value plus _set.all()
  #   items = order.orderitem_set.all()
  # else:
  #   items = []
  #   order = {'get_cart_total':0,'get_cart_items':0}
  # # count_items = items.count()
  # # count_items = items.aggregate(qty=Sum(F("quantity")))
  # # total = items.aggregate(total=Sum(F("product__price")*F("quantity")))
  # context = {
  #   'items':items,
  #   'order':order,
    # 'count_items':count_items,
    # 'total':total['total'],
  # }
  return render(request,'store/cart.html')

def checkout(request):
  context = {}
  return render(request,'store/checkout.html',context)
