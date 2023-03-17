
from django.http import JsonResponse
from django.shortcuts import render,redirect,get_object_or_404
# from home.models import *
from .models import *
from twilio.rest import Client
from unicodedata import category

import datetime
import json


# Create your views here.


def payments(request):
    body = json.loads(request.body)
    order = Order.objects.get(user=request.user, is_ordered=False, order_number=body['orderID'])

    # Store transaction details inside Payment model
    payment = Payment(
        user = request.user,
        payment_id = body['transID'],
        payment_method = body['payment_method'],
        amount_paid = order.order_total,
        status = body['status'],
    )
    payment.save()

    order.payment = payment
    order.is_ordered = True
    order.save()

    # Move the cart items to Order Product table
    cart_items = CartItem.objects.filter(user=request.user)

    for item in cart_items:
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id
        orderproduct.payment = payment
        orderproduct.user_id = request.user.id
        orderproduct.product_id = item.product.id
        orderproduct.quantity = item.quantity
        orderproduct.product_price = item.product.price_for_min_quantity
        orderproduct.ordered = True
        orderproduct.save()
        # Reduce the quantity of the sold products
        product = Product.objects.get(id=item.product_id)
        product.available_quantity -= item.quantity
        product.save()

    # Clear cart
    CartItem.objects.filter(user=request.user).delete()

    # Send order recieved email to customer
    # mail_subject = 'Thank you for your order!'
    # message = render_to_string('orders/order_recieved_email.html', {
    #     'user': request.user,
    #     'order': order,
    # })
    # to_email = request.user.email
    # send_email = EmailMessage(mail_subject, message, to=[to_email])
    # send_email.send()

    # Send order number and transaction id back to sendData method via JsonResponse
    def send_order(mobile):
        print("FUNCTION CALLED")
        # account_sid = 'AC5da717c5d9ef46b543a1dd7ef811d0c9'
        # auth_token = 'f9884ec91a0034fceefbe67e7b32a7d4'
        client = Client(account_sid, auth_token)

        message = client.messages.create(
                                                        body=f'Your order is placed successfully',
                                                        from_='+15739953871',
                                                        to=f'+91{mobile}')

        print(message.body)
        return None
    print(order.phone)
    send_order(order.phone)

    data = {
        'order_number': order.order_number,
        'transID': payment.payment_id,
    }
    return JsonResponse(data)

def place_order(request, total=0, quantity=0):
    print("place_ordeer invoked")
    current_user = request.user

    # If the cart count is less than or equal to 0, then redirect back to shop
    cart_items = CartItem.objects.filter(user=current_user)
    # cart_count = len(cart_items)
    # if cart_count <= 0:
    #     return redirect('store')

    grand_total = 0
   

    for cart_item in cart_items:
        print("}}}}}}}}}}}}}}}}}}",cart_item.product.discount,   cart_item.quantity)
        total += (cart_item.product.discount * cart_item.quantity)
        quantity += cart_item.quantity
    grand_total = total 

    if request.method == 'POST':
            # Store all the billing information inside Order table
            data = Order()
            data.user = current_user
            data.name = request.POST['name']
            data.phone = request.POST['phone']
            data.email = request.POST['email']
            data.address_line = request.POST['address_line_1']
            data.state = request.POST['state']
            data.city = request.POST['city']
            data.order_total = grand_total
            # Generate order number
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr,mt,dt)
            current_date = d.strftime("%Y%m%d") #20210305
            order_number = current_date
            data.order_number = order_number
            print(data.id)
            data.save()
            data.order_number = order_number+str(data.id)
            print(data.id)

            data.save()

            orders = Order.objects.get(user=current_user, is_ordered=False,id=data.id)
            print(orders.name)
            print(cart_items)
            
            context = {
                        'order': orders,
                        'cart_items': cart_items,
                        'total': total,
                        'grand_total': grand_total,
                    }
            return render(request,'payments/payment.html',context)
    else:
        return redirect('checkout')


def order_complete(request):
    order_number = request.GET.get('order_number')
    transID = request.GET.get('payment_id')

    try:
        order = Order.objects.get(order_number=order_number, is_ordered=True)
        ordered_products = OrderProduct.objects.filter(order_id=order.id)
        print("|||||||||||||||||||||",ordered_products)

        subtotal = 0
        for i in ordered_products:
            print(i.product_price, i.quantity)
            subtotal += i.product_price * i.quantity

        payment = Payment.objects.get(payment_id=transID)

        context = {
            'order': order,
            'ordered_products': ordered_products,
            'order_number': order.order_number,
            'transID': payment.payment_id,
            'payment': payment,
            'subtotal': subtotal,
        }
        return render(request, 'payments/order_complete.html', context)
    except (Payment.DoesNotExist, Order.DoesNotExist):
        return redirect('home')
