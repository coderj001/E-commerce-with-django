from core.views import homepage
from django.urls import path

app_name='core'

urlpatterns = [
    path('home/',homepage,name="homepage"),
    path('',homepage,name="homepage"),
]
