from .models import * 
import json


def CartCookie(request):
    try:
            cart = json.loads(request.COOKIES['cart'])
    except:
            cart = {}
    items = []
    order = {'get_items_quantity':0,'get_items_price':0,'':False}
    cartitems = order['get_items_quantity']
    for i in cart:
        try:
            cartitems += cart[i]['quantity']
            product = Product.objects.get(id = i)
            total = product.price * cart[i]['quantity']
            order['get_items_price'] += total
            order['get_items_quantity'] += cart[i]['quantity']

            item = {
                'product' : {
                    'id':product.id,
                    'name':product.name,
                    'price':product.price,
                    'imageURL':product.imageURL
                },
                'quantity':cart[i]['quantity'],
                'get_total' : total

            }
            items.append(item)
            print(items)
            
        except:
            pass
    return {'items':items,'order':order,'quant':cartitems}

def cartData(request):
    if request.user.is_authenticated:
            customer = request.user.customer
            order,created = Order.objects.get_or_create(customer = customer,complete = False)
            items = order.orderitem_set.all()
            context={'items':items,'order':order,"quant":order.get_items_quantity}
    else:   
        cartData = CartCookie(request)
        items = cartData['items']
        cartitems = cartData['quant']
        order = cartData['order']
        context={'items':items,"quant": cartitems,'order':order}
    return context


def guestOrder(request,data):
    cookies = request.COOKIES
    name = data['user']['name']
    email= data['user']['email']

    cookieData = CartCookie(request)
    items = cookieData['items']

    customer,created = Customer.objects.get_or_create(email = email)
    customer.name = name
    customer.save()

    order = Order.objects.create(customer = customer, complete = False)
    for item in items:
        product = Product.objects.get(id = item['product']['id'])
        orderItem = OrderItem.objects.create(product = product, Order = order,quantity = item['quantity'])

    return order,customer