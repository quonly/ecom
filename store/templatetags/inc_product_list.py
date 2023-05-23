from django import template
from store.models import *

register = template.Library()
@register.inclusion_tag('store/product_list.html')
def product_list(customer):
  if customer:
    order, created = Order.objects.get_or_create(customer=customer,complete=False)
    items = order.orderitem_set.all()
  else:
    items = []
    order = {'get_cart_total':0,'get_cart_items':0}
  return  {
      'items':items,
      'order':order,
         }
  
