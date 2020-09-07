from core.models import Item, Order, OrderItem
from django.shortcuts import render


def homepage(request):
    context = {
            "Items": Item.objects.all()
        }
    return render(request, "core/homepage.html", context)


def checkoutpage(request):
    context = {}
    return render(request, "core/checkoutpage.html", context)


def productpage(request):
    context = {}
    return render(request, "core/productpage.html", context)
