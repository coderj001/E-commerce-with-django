from core.forms import CheckOutForm
from core.models import BillingAddress, Item, Order, OrderItem
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

class CheckOutPage(View):

    def get(self, request, *args, **kwargs):
        form = CheckOutForm()
        context = { 'form': form }
        return render(request, "core/checkoutpage.html", context)

    def post(self, request, *args, **kwargs):
        form = CheckOutForm(request.POST or None)
        try:
            order = Order.objects.get(user=request.user, ordered=False)
            if form.is_valid():
                street_address = form.cleaned_data.get('street_address ')
                apparment_address = form.cleaned_data.get('apparment_address ')
                country = form.cleaned_data.get('country')
                zipcode = form.cleaned_data.get('zipcode')
                # TODO: add functionality for there fields
                # same_shipping_address = form.cleaned_data.get('same_shipping_address ')
                # save_info = form.cleaned_data.get('save_info ')
                payment_option = form.cleaned_data.get('payment_option ')
                billing_address=BillingAddress(
                        user = request.user,
                        street_address = street_address,
                        country = country,
                        zipcode = zipcode,
                        )
                billing_address.save()
                order.billing_address = billing_address
                order.ordered = True
                # TODO: redirect to selected payment options
                return redirect('core:checkoutpage')
            messages.info(request, "Failed to checkout.")
            return redirect('core:checkoutpage')
        except ObjectDoesNotExist:
            messages.error(request, 'Order does not exist.')
            return redirect("core:homepage")

class PaymentView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'core/payment.html')

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
            return redirect("core:order-summery")
        else:
            order.items.add(order_item)
            messages.info(request, "This item was add to your cart.")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "Item was added to your cart.")
        return redirect("core:productpage", slug=slug)
    return redirect("core:order-summery")

@login_required
def remove_from_cart(request,slug):
    item = get_object_or_404(Item,slug=slug)
    order_qs = Order.objects.filter(user=request.user,ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(item=item,user=request.user,ordered=False)[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, "This item was removed from your cart.")
        else:
            messages.info(request, "Item didn't previously exist.")
            return redirect("core:productpage", slug=slug)
    else:
        messages.info(request, "You don't have active order.")
        return redirect("core:productpage", slug=slug)
    return redirect("core:productpage", slug=slug)

@login_required
def remove_single_item_from_cart(request,slug):
    item = get_object_or_404(Item,slug=slug)
    order_qs = Order.objects.filter(user=request.user,ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(item=item,user=request.user,ordered=False)[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
                order_item.delete()
            messages.info(request, "This Item quantity was updated.")
            return redirect("core:order-summery")
        else:
            messages.info(request, "Item didn't previously exist.")
            return redirect("core:productpage", slug=slug)
    else:
        messages.info(request, "You don't have active order.")
        return redirect("core:productpage", slug=slug)
    return redirect("core:productpage", slug=slug)
