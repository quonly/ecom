import json
from .models import *

def cookieCart(request):
  try:
    cart = json.loads(request.COOKIES['cart']) # Deserialize s (a str, bytes or bytearray instance containing a JSON document) to a Python object.
  except:
    cart = {}
    
  items = []
  order = {'get_cart_total':0,'get_cart_items':0,'shipping':False}
  cartItems = order['get_cart_items']
  for i in cart:
    try:
      quantity = cart[i]['quantity']
      cartItems += quantity
      product = Product.objects.get(id=i)
      total = (product.price * quantity)

      order['get_cart_total']+= total
      order['get_cart_items'] += quantity

      item = {
        'product':{
          'id':product.id,
          'name':product.name,
          'price':product.price,
          'imageUrl':product.imageUrl,
        },
        'quantity': quantity,
        'get_total': total,
      }
      items.append(item)

      if product.digital == False:
        order['shipping'] = True
    except:
      pass
  return {'cartItems':cartItems,'order':order,'items':items}

def cartDdata(request):
  if request.user.is_authenticated:
    customer = request.user.customer
    order, created = Order.objects.get_or_create(customer=customer,complete=False)
    items = order.orderitem_set.all()
    cartItems = order.get_cart_items
  else:
    cookieData = cookieCart(request)
    cartItems = cookieData['cartItems']
    order = cookieData['order']
    items = cookieData['items']
  return {
    'items':items,
    'order':order,
    'cartItems':cartItems,
  }