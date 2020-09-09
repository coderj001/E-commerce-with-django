from core.views import (CheckOutPage, HomePageView, OrderSummeryView,
                        ProductPageView, add_to_cart, remove_from_cart,
                        remove_single_item_from_cart)
from django.urls import path

app_name='core'

urlpatterns = [
    path('home/',HomePageView.as_view(),name="homepage"),
    path('',HomePageView.as_view(),name="homepage"),
    path('product/<slug>/',ProductPageView.as_view(),name="productpage"),
    path('checkout/',CheckOutPage.as_view(),name="checkoutpage"),
    path('order_summery/',OrderSummeryView.as_view(),name="order-summery"),
    path('add_to_cart/<slug>/',add_to_cart,name="add-to-cart"),
    path('remove_from_cart/<slug>/',remove_from_cart,name="remove-from-cart"),
    path('remove_single_item_from_cart/<slug>/',remove_single_item_from_cart,name="remove-single-item-from-cart"),
]
