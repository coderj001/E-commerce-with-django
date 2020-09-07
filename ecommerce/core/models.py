import uuid

from django.conf import settings
from django.db import models


class Item(models.Model):
    id=models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    title=models.CharField(max_length=255,blank=False,verbose_name="Item title")
    price=models.FloatField(verbose_name="Item price")

    def __str__(self):
        return self.title

class OrderItem(models.Model):
    id=models.AutoField(primary_key=True,editable=False)
    item=models.ForeignKey(Item, on_delete=models.CASCADE)

class Order(models.Model):
    id=models.UUIDField(primary_key=True,editable=False,default=uuid.uuid5)
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    items=models.ManyToManyField(OrderItem)
    ordered_date=models.DateTimeField(auto_now_add=True)
    ordered=models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
