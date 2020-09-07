import uuid

from django.conf import settings
from django.db import models

CATAGORY_CHOICES=(
        ('S','Shirt'),
        ('SW','Sport Wear'),
        ('OW','Outwear'),
        )

LABEL_CHOICES=(
        ('P','primary'),
        ('S','secondary'),
        ('D','danger'),
        )

class Item(models.Model):
    id=models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    title=models.CharField(max_length=255,blank=False,verbose_name="Item title")
    price=models.FloatField(verbose_name="Item price")
    category=models.CharField(max_length=2,choices=CATAGORY_CHOICES,verbose_name="Select category of product")
    label=models.CharField(max_length=1,choices=LABEL_CHOICES,verbose_name="Select level of product")

    def __str__(self):
        return self.title

class OrderItem(models.Model):
    id=models.AutoField(primary_key=True,editable=False)
    item=models.ForeignKey(Item, on_delete=models.CASCADE)
    def __str__(self):
        return self.id

class Order(models.Model):
    id=models.UUIDField(primary_key=True,editable=False,default=uuid.uuid5)
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    items=models.ManyToManyField(OrderItem)
    ordered_date=models.DateTimeField(auto_now_add=True)
    ordered=models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
