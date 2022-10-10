from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('',store,name='home'),
    path('cart/',cart,name='cart'),
    path('checkout/',checkout,name='checkout'),
    path('update_orderitem/',update_item,name='update_item'),
    path('process_order/',processOrder,name='update_item'),
]