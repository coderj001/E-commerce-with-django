from core.models import Item, Order, OrderItem
from django.shortcuts import render


def demo(request):
    items=Item.objects.all()
    context={ 'items':items }
    return render(request,"core/demo.html",context)
