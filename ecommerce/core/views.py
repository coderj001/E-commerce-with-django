from core.models import Item, Order, OrderItem
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.generic import DetailView, ListView, View


class HomePageView(ListView):
    model = Item
    context_object_name = 'items'
    paginate_by = 10
    template_name = "core/homepage.html"

class OrderSummeryView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        try:
            order=Order.objects.get(user=request.user, ordered=False)
            context = {'order':order}
        except ObjectDoesNotExist:
            messages.error(request, "You do not have an active order.")
            return redirect("core:homepage")
        return render(request, "core/ordersummery.html", context)


class ProductPageView(DetailView):
    model = Item
    context_object_name = 'item'
    template_name = "core/productpage.html"

def checkoutpage(request):
    context = {}
    return render(request, "core/checkoutpage.html", context)

@login_required
def add_to_cart(request,slug):
    item = get_object_or_404(Item,slug=slug)
    order_item, created = OrderItem.objects.get_or_create(item=item,user=request.user,ordered=False)
    order_qs = Order.objects.filter(user=request.user,ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity+=1
            order_item.save()
            messages.info(request, "This item quantity increased by one.")
        else:
            order.items.add(order_item)
            messages.info(request, "This item was add to your cart.")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "Item was added to your cart.")
    return redirect("core:productpage", slug=slug)

@login_required
def remove_from_cart(request,slug):
    item = get_object_or_404(Item,slug=slug)
    order_qs = Order.objects.filter(user=request.user,ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(item=item,user=request.user,ordered=False)[0]
            order.items.remove(order_item)
            messages.info(request, "This item was removed from your cart.")
        else:
            messages.info(request, "Item didn't previously exist.")
            return redirect("core:productpage", slug=slug)
    else:
        messages.info(request, "You don't have active order.")
        return redirect("core:productpage", slug=slug)
    return redirect("core:productpage", slug=slug)
