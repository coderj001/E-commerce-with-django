import stripe
from core.forms import CheckOutForm
from core.models import BillingAddress, Coupon, Item, Order, OrderItem, Payment
from django.conf import settings
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
            order = Order.objects.get(user=request.user, ordered=False)
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
        order = Order.objects.get(user=request.user, ordered=False)
        context = {'form': form, 'order': order}
        return render(request, "core/checkoutpage.html", context)

    def post(self, request, *args, **kwargs):
        form = CheckOutForm(request.POST or None)
        try:
            order = Order.objects.get(user=request.user, ordered=False)
            if form.is_valid():
                street_address = form.cleaned_data.get('street_address')
                apparment_address = form.cleaned_data.get('apparment_address')
                country = form.cleaned_data.get('country')
                zipcode = form.cleaned_data.get('zipcode')
                # TODO: add functionality for there fields
                # same_shipping_address = form.cleaned_data.get('same_shipping_address ')
                # save_info = form.cleaned_data.get('save_info ')
                payment_option = form.cleaned_data.get('payment_option')
                billing_address=BillingAddress(
                        user=request.user,
                        street_address=street_address,
                        country=country,
                        zipcode=zipcode,
                        )
                billing_address.save()
                order.billing_address = billing_address
                order.ordered = True
                # TODO: redirect to selected payment options
                if payment_option == 'S':
                    return redirect('core:payment', payment_option='stripe')
                if payment_option == 'P':
                    return redirect('core:payment', payment_option='paypal')
                else:
                    messages.info(request, "Invalid Payment Options.")
                    return redirect('core:checkoutpage')
            messages.info(request, "Failed to checkout.")
            return redirect('core:checkoutpage')
        except ObjectDoesNotExist:
            messages.error(request, 'Order does not exist.')
            return redirect("core:homepage")

class PaymentView(View):

    def get(self, request, *args, **kwargs):
        order = Order.objects.get(user=request.user, ordered=False)
        context = {
                'order': order
            }
        return render(request, 'core/payment.html', context=context)

    def post(self, request, *args, **kwargs):
        order = Order.objects.get(user=request.user, ordered=False)
        token = request.POST.get('stripeToken')
        stripe.api_key = settings.STRIPE_SECRET_KEY
        amount = int(order.get_total())

        try:
            charge = stripe.Charge.create(
                    description="Software development services",
                    source=token,
                    amount=amount,
                    currency="inr",
                )
            # Create Payment
            payment = Payment()
            payment.stripe_charge_id = charge['id']
            payment.user = self.request.user
            payment.amount = order.get_total()
            payment.save()

            order_items = order.items.all()
            order_items.update(ordered=True)
            for item in order_items:
                item.save()

            order.ordered = True
            order.payment = payment
            order.save()
            messages.info(request, "Your order successfull")
            return redirect("core:homepage")
        except stripe.error.CardError as e:
          # Since it's a decline, stripe.error.CardError will be caught

          print('Status is: %s' % e.http_status)
          print('Type is: %s' % e.error.type)
          print('Code is: %s' % e.error.code)
          # param is '' in this case
          print('Param is: %s' % e.error.param)
          print('Message is: %s' % e.error.message)
          messages.info(request, e.error.message)
          return redirect("core:homepage")
        except stripe.error.RateLimitError as e:
          # Too many requests made to the API too quickly
          messages.info(request, "Rate limit error")
          return redirect("core:homepage")
        except stripe.error.InvalidRequestError as e:
          # Invalid parameters were supplied to Stripe's API
          messages.info(request, "Invalid parameters")
          return redirect("core:homepage")
        except stripe.error.AuthenticationError as e:
          # Authentication with Stripe's API failed
          # (maybe you changed API keys recently)
          messages.info(request, "Not Authentication")
          return redirect("core:homepage")
        except stripe.error.APIConnectionError as e:
          # Network communication with Stripe failed
          messages.info(request, "Network EOFError")
          return redirect("core:homepage")
        except stripe.error.StripeError as e:
          # Display a very generic error to the user, and maybe send
          # yourself an email
          messages.info(request, "Something went wrong. Your are not charges. Please try again after sometime.")
          return redirect("core:homepage")
        except Exception as e:
            # TODO: Send email to ourself
            messages.info(request, "Serious error occurred. We have been notified.")
            return redirect("core:homepage")

            


@login_required
def add_to_cart(request, slug):
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
def remove_from_cart(request, slug):
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
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(item=item, user=request.user, ordered=False)[0]
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

def get_coupon(request, code):
    try:
        coupon = Coupon.objects.get(code=code)
        return coupon
    except:
        messages.info(request, "This coupon is not valid.")
        return redirect("core:checkoutpage")

def add_coupon(request, code):
    try:
        order = Order.objects.get(user=request.user, ordered=False)
        order.coupon = get_coupon(request,code)
        order.save()
        messages.success(request, "Successfully added coupon.")
        return redirect("core:checkoutpage")
    except:
        messages.info(request, "You don't have active order")
        return redirect("core:checkoutpage")
