from core.models import Item, Order, OrderItem
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
