from django import template
from store.models import *

register = template.Library()

# order =  {}

@register.inclusion_tag('store/product_list.html')
def product_list(items):
  return  {'items':items,}

@register.inclusion_tag('store/summary.html')
def summary(order):
  print(order)
  return {'order':order}
    