from django.shortcuts import render, redirect,get_object_or_404
from .models import Cart,CartItem
from order.models import Order,OrderItem
from shop.models import Product
from django.core.exceptions import ObjectDoesNotExist
import stripe
from django.conf import settings


# Create your views here.
def cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_cart(request,product_id):
    product = Product.objects.get(id=product_id)
    try:
        cart = Cart.objects.get(cart_id=cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=cart_id(request))
        cart.save()
    try:
        cart_item = CartItem.objects.get(product=product,cart=cart)
        if cart_item.quantity < cart_item.product.stock:
           cart_item.quantity +=1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item =CartItem.objects.create(cart=cart,product=product,quantity =1)
        cart_item.save()

    return redirect('cart:cart_detail')

def cart_detail(request,cart_items=None,total =0,counter=0):



    try:
        cart = Cart.objects.get(cart_id=cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart,active=True)
        for item in cart_items:
            total = total + item.quantity*item.product.price
            counter = counter + item.quantity
    except ObjectDoesNotExist:
        pass

    stripe.api_key = settings.STRIPE_SECRET_KEY
    stripe_total = int(total * 100)
    description = 'Vkart -New Order'
    data_key =settings.STRIPE_PUBLISHABLE_KEY
    if request.method =='POST' :
        # print(request.POST)
        try:
            token = request.POST['stripeToken']

            email = request.POST['stripeEmail']
            billingName = request.POST['stripeBillingName']
            billingAddress = request.POST['stripeBillingAddressLine1']
            billingcity = request.POST['stripeBillingAddressCity']
            billingPostcode = request.POST['stripeBillingAddressZip']
            billingCountry = request.POST['stripeBillingAddressCountryCode']
            shippingName = request.POST['stripeShippingName']
            shippingAddress = request.POST['stripeShippingAddressLine1']
            shippingCity = request.POST['stripeShippingAddressCity']
            shippingPostcode = request.POST['stripeShippingAddressZip']
            shippingCountry = request.POST['stripeShippingAddressCountryCode']
            customer = stripe.Customer.create(email=email,source=token)
            charge = stripe.Charge.create(amount=stripe_total,currency='inr',description=description,customer=customer.id)
            # creating order
            try:
                order_details = Order.objects.create(
                    token = token,
                    total = total,
                    emailAddress = email,
                    billingName = billingName,
                    billingAddress = billingAddress,
                    billingCity = billingcity,
                    billingPostcode = billingPostcode,
                    billingCountry = billingCountry,
                    shippingName = shippingName,
                    shippingAddress =shippingAddress,
                    shippingCity = shippingCity,
                    shippingPostcode = shippingPostcode,
                    shippingCountry = shippingCountry)
                order_details.save()
                for item in cart_items:
                    oi = OrderItem.objects.create(
                        product = item.product.name,
                        quantity = item.quantity,
                        price = item.product.price,
                        order = order_details
                    )
                    oi.save()
                    products = Product.objects.get(id=item.product.id)
                    products.stock = int(item.product.stock-item.quantity)
                    products.save()
                    item.delete()
                    print("The order is created successfully")
                return redirect('order:thanks',order_details.id)
            except ObjectDoesNotExist:
                pass



        except stripe.error.CardError as e:
                    return False,e


    return render(request,'cart_detail.html',{'cart_items':cart_items,'total':total,'counter':counter,'data_key':data_key,'stripe_total':stripe_total,'description':description})



def counter(request):
    item_count=0
    if 'admin' in request.path:
        return {}
    else:
        try:
            cart = Cart.objects.filter(cart_id=cart_id(request))
            cart_item = CartItem.objects.all().filter(cart=cart[:1])
            for item in cart_item:
                item_count += item.quantity
        except Cart.DoesNotExist:
            item_count=0
    return dict(item_count=item_count)

def cart_remove(request,product_id):
    cart = Cart.objects.get(cart_id=cart_id(request))
    product = get_object_or_404(Product,id=product_id)
    cart_item = CartItem.objects.get(product=product,cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -=1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart:cart_detail')


def cart_delete(request,product_id):
    cart = Cart.objects.get(cart_id=cart_id(request))
    product = get_object_or_404(Product,id=product_id)
    cart_item = CartItem.objects.get(product=product,cart=cart)

    cart_item.delete()
    return redirect('cart:cart_detail')
















