from core.models import (BillingAddress, Coupon, Item, Order, OrderItem,
                         Payment, Refund)
from django.contrib import admin


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    pass


@admin.register(OrderItem)
class ItemOrderItem(admin.ModelAdmin):
    pass


def make_refund_accepted(modeladmin, request, queryset):
    queryset.update(refund_requested=False, refund_granted=True)

make_refund_accepted.short_description = 'update orders to refund granted'

@admin.register(Order)
class ItemOrder(admin.ModelAdmin):
    list_display = ['user', 'ordered_date', 'ordered', 'being_delivered', 'received', 'refund_requested', 'refund_granted','billing_address', 'payment', 'coupon']
    list_display_links = ['user', 'billing_address', 'payment', 'coupon']
    list_filter = ['ordered', 'being_delivered', 'received', 'refund_requested', 'refund_granted']
    ordering = ('-ordered_date',)
    search_fields = ['user__username', 'ref_code']
    actions = [make_refund_accepted]

@admin.register(BillingAddress)
class AdminBillingAddress(admin.ModelAdmin):
    pass

@admin.register(Payment)
class AdminPayment(admin.ModelAdmin):
    pass

@admin.register(Coupon)
class AdminCoupon(admin.ModelAdmin):
    pass

@admin.register(Refund)
class AdminRefund(admin.ModelAdmin):
    pass
