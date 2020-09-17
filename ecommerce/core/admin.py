from core.models import BillingAddress, Item, Order, OrderItem, Payment
from django.contrib import admin


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    pass


@admin.register(OrderItem)
class ItemOrderItem(admin.ModelAdmin):
    pass


@admin.register(Order)
class ItemOrder(admin.ModelAdmin):
    pass

@admin.register(BillingAddress)
class AdminBillingAddress(admin.ModelAdmin):
    pass

@admin.register(Payment)
class AdminPayment(admin.ModelAdmin):
    pass
