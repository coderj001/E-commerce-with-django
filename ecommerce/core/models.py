import uuid

from django.conf import settings
from django.db import models
from django.shortcuts import reverse
from django_countries.fields import CountryField
from django_extensions.db.fields import AutoSlugField

CATAGORY_CHOICES = (
    ('S', 'Shirt'),
    ('SW', 'Sport Wear'),
    ('OW', 'Outwear'),
)

LABEL_CHOICES = (
    ('P', 'primary'),
    ('S', 'secondary'),
    ('D', 'danger'),
)


class Item(models.Model):

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    title = models.CharField(
        max_length=255, blank=False, verbose_name="Item title")
    price = models.FloatField(verbose_name="Item price")
    discount_price = models.FloatField(
        blank=True, null=True, verbose_name="Item discount price")
    category = models.CharField(
        max_length=2, choices=CATAGORY_CHOICES,
        verbose_name="Select category of product")
    label = models.CharField(
        max_length=1, choices=LABEL_CHOICES,
        verbose_name="Select level of product")
    slug = models.SlugField(
        max_length=255, verbose_name="slug field", editable=False)
    slug = AutoSlugField(('slug'), max_length=255,
                         unique=True, populate_from=('title', 'id'))
    description = models.TextField()
    image = models.ImageField(default="default_card.jpg")

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.id

    def get_absolute_url(self):
        return reverse("core:productpage", kwargs={'slug': self.slug})

    def get_add_to_cart_url(self):
        return reverse("core:add-to-cart", kwargs={'slug': self.slug})

    def get_remove_from_cart_url(self):
        return reverse("core:remove-from-cart", kwargs={'slug': self.slug})


class OrderItem(models.Model):

    id = models.AutoField(primary_key=True, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return "{} of {}".format(self.quantity, self.item.title)

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_item_dicount_price(self):
        return self.quantity * self.item.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_item_dicount_price()

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_item_dicount_price()
        return self.get_total_item_price()


class Order(models.Model):

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid1)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ref_code = models.CharField(max_length=20)
    items = models.ManyToManyField(OrderItem)
    ordered_date = models.DateTimeField(auto_now_add=True, editable=True)
    ordered = models.BooleanField(default=False)
    billing_address = models.ForeignKey(
        'BillingAddress', on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey(
        'Payment', on_delete=models.SET_NULL, blank=True, null=True)
    coupon = models.ForeignKey(
        'Coupon', on_delete=models.SET_NULL, blank=True, null=True)
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        if self.coupon:
            total -= self.coupon.amount
        return total

    '''
    Order Lifecycle
    1. Item added to cart
    2. Added billing address to cart
    (Failed Checkout)
    3. Payment
    (Preprocessing, processing, packaging etc.)
    4. Begin delivered
    5. Recived
    6. Refunds
    '''


class BillingAddress(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    street_address = models.CharField(max_length=255)
    country = CountryField(multiple=True)
    zipcode = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username


class Payment(models.Model):

    stripe_charge_id = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Coupon(models.Model):

    code = models.CharField(max_length=15)
    amount = models.FloatField()

    def __str__(self):
        return self.code


class Refund(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    reason = models.TextField()
    accepeted = models.BooleanField(default=False)
    email = models.EmailField()

    def __str__(self):
        return f"{self.id}"
