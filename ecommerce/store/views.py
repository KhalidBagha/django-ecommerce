from itertools import product
from math import prod
from django.shortcuts import render
from .models import * 
from django.http import JsonResponse
import json
import datetime
from .utils import *
# Create your views here.

def store(request):
    product = Product.objects.all()
    x = 0
    if request.user.is_authenticated:
        customer = request.user.customer
        x, created= Order.objects.get_or_create(customer = customer,complete = False)
        x=x.get_items_quantity
    else:
        try:
            cart = json.loads(request.COOKIES['cart'])
        except:
            cart = {}
        items = []
        order = {'get_items_quantity':0,'get_items_price':0,'':False}
        x = order['get_items_quantity']
        for i in cart:
            x += cart[i]['quantity']



    context={'products':product,"quant": x}

    return render(request,'store.html',context)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order,created = Order.objects.get_or_create(customer = customer,complete = False)
        orderitems = order.orderitem_set.all()
        context={'items':orderitems,'order':order,"quant":order.get_items_quantity}
    else:   
        cartData = CartCookie(request)
        items = cartData['items']
        cartitems = cartData['quant']
        order = cartData['order']
        context={'items':items,"quant": cartitems,'order':order}
        print(items)
    return render(request,'cart.html',context)
    

def checkout(request):
    # if request.user.is_authenticated:
    #         customer = request.user.customer
    #         order,created = Order.objects.get_or_create(customer = customer,complete = False)
    #         items = order.orderitem_set.all()
    #         context={'items':items,'order':order,"quant":order.get_items_quantity}
    # else:   
    #     cartData = CartCookie(request)
    #     items = cartData['items']
    #     cartitems = cartData['quant']
    #     order = cartData['order']
    #     context={'items':items,"quant": cartitems,'order':order}

    data = cartData(request)

    return render(request,'checkout.html',data)

def update_item(request):
    
    data = json.loads(request.body)
    product_id = data['product_id']
    action = data['action']

    customer = request.user.customer
    product = Product.objects.get(id=product_id)

    print(product,customer)

    checkOrder = Order.objects.filter(customer= customer).count()
    print(checkOrder)
    if checkOrder == 0:
        ordercreated = Order.objects.create(customer= customer,status = "Pending",transactionID = "322342ISAD",complete = False)
        print(ordercreated.id,ordercreated.customer)
        orderItemCreate = OrderItem.objects.create(product=product,Order=ordercreated,quantity=int(1))
        orderItemCreate.save()
        print(orderItemCreate,ordercreated)
    else:
        order = Order.objects.get(customer= customer,complete = False)
        orderItemCheck = OrderItem.objects.filter(product = product, Order=order).count()
        if orderItemCheck : 
            items = OrderItem.objects.get(product = product, Order=order)
            if action == "add":
                 items.quantity += 1
            elif action == "remove":
                  items.quantity -= 1
            items.save()
        
            if items.quantity == 0:
                    items.delete() 
        else:
            orderItemCreate = OrderItem.objects.create(product=product,Order=order,quantity=int(1))
            orderItemCreate.save()
            
    print(checkOrder)
    # order, create = Order.objects.get_or_create(customer = customer)
    # orderitem, create = OrderItem.objects.get_or_create(Order = order, product = product)
    # if action == "add":
    #     orderitem.quantity += 1
    # elif action == "remove":
    #     orderitem.quantity -= 1

    # orderitem.save()

    # if orderitem.quantity <= 0:
    #     orderitem.delete()    


    action = data['action']
    # print(product_id,action)
    return JsonResponse("Item Added",safe=False)


def processOrder(request):
    t_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer= customer, complete = False)
    

    else:
        order,customer = guestOrder(request,data)
    total = float(data['user']['total'])
    if total == order.get_items_price:
            order.complete = True
            order.transactionID = str(t_id) 
    order.save()
    shipping = Shipping.objects.create(customer = customer,Order = order ,city = data['shipping']['city'],zipcode = data['shipping']['zipcode'],address = data['shipping']['address'],state = data['shipping']['state'])
    shipping.save()

    return JsonResponse("Order Processed", safe = False)

