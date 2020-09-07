from core.views import checkoutpage, homepage, productpage
from django.urls import path

app_name='core'

urlpatterns = [
    path('home/',homepage,name="homepage"),
    path('',homepage,name="homepage"),
    path('product/',productpage,name="productpage"),
    path('checkout/',checkoutpage,name="checkoutpage"),
]
