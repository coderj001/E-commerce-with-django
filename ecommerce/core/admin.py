from core.models import BillingAddress, Coupon, Item, Order, OrderItem, Payment
from django.contrib import admin


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    pass


@admin.register(OrderItem)
class ItemOrderItem(admin.ModelAdmin):
    pass


@admin.register(Order)
class ItemOrder(admin.ModelAdmin):
    list_display = ['user', 'ordered_date', 'ordered', 'being_delivered', 'received', 'refund_requested', 'refund_granted','billing_address', 'payment', 'coupon']
    list_display_links = ['user', 'billing_address', 'payment', 'coupon']
    list_filter = ['ordered', 'being_delivered', 'received', 'refund_requested', 'refund_granted']
    ordering = ('-ordered_date',)
    search_fields = ['user__username', 'ref_code']

@admin.register(BillingAddress)
class AdminBillingAddress(admin.ModelAdmin):
    pass

@admin.register(Payment)
class AdminPayment(admin.ModelAdmin):
    pass

@admin.register(Coupon)
class AdminCoupon(admin.ModelAdmin):
    pass
