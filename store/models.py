from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Customer(models.Model):
  user = models.OneToOneField(User,null=True,blank=True,on_delete=models.CASCADE)
  name = models.CharField(max_length=200,null=True)
  email = models.EmailField(max_length=200)

  def __str__(self):
    return self.name
  
class Product(models.Model):
  name = models.CharField(max_length=200,null=True)
  price = models.DecimalField(max_digits=6,decimal_places=2)
  digital = models.BooleanField(default=False,null=True,blank=False)
  #image
  image = models.ImageField(null=True,blank=True,)

  @property
  def imageUrl(self):
    try:
      url = self.image.url
    except:
      url = ''
    return url
  
  def __str__(self):
    return self.name

class Order(models.Model):
  customer = models.ForeignKey('Customer',on_delete=models.SET_NULL,null=True,blank=True)
  date_ordered = models.DateTimeField(auto_now_add=True)
  complete = models.BooleanField(default=False) # หากเป็น False จะเพิ่มสินค้าเข้ามาได้เรื่อยๆ 
  transaction_id = models.CharField(max_length=200,null=True) # null=True หมายความว่าสามารถปล่อยว่างเวลาสร้างได้ แต่เวลาไปเพิ่มข้อมูลในหน้าแอดมินหรือฟอร์มจะต้องใส่ค่าด้วย

  @property
  def shipping(self):
    shipping = False
    orderItems = self.orderitem_set.all()
    for i in orderItems:
      if i.product.digital == False:
        shipping = True
        
    return shipping

  @property
  def get_cart_total(self):
    orderitems = self.orderitem_set.all()
    total = sum([item.get_total for item in orderitems])
    return total
  
  @property
  def get_cart_items(self):
    orderitems = self.orderitem_set.all()
    total = sum([item.quantity for item in orderitems])
    return total
  
  def __str__(self):
    return str(self.id)

class OrderItem(models.Model):
  product = models.ForeignKey('Product',on_delete=models.SET_NULL,null=True,blank=True)
  order = models.ForeignKey('Order',on_delete=models.SET_NULL,null=True,blank=True)
  quantity = models.IntegerField(default=0,blank=True)
  date_added = models.DateTimeField(auto_now_add=True)
  
  @property
  def get_total(self):
    total = self.product.price * self.quantity
    return total
  
  def __str__(self):
    return self.product.name

class ShippingAddress(models.Model):
  customer = models.ForeignKey('Customer',on_delete=models.SET_NULL,null=True,blank=True)
  order = models.ForeignKey('Order',on_delete=models.SET_NULL,null=True,blank=True)
  address = models.CharField(max_length=200,null=True)
  city = models.CharField(max_length=200,null=True)
  state = models.CharField(max_length=200,null=True)
  zipcode = models.CharField(max_length=200,null=True)
  date_added = models.DateTimeField(auto_now_add=True)
  
  def __str__(self):
    return self.address