from django.shortcuts import render
from account.models import Profile
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart


# from .tasks import order_created


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                for size_item_key in item['size_items'].keys():
                    size_item_value = item['size_items'][size_item_key]
                    OrderItem.objects.create(order=order,
                                             product=item['product'],
                                             price=item['price'],
                                             quantity=size_item_value[
                                                 'quantity'],
                                             size=size_item_key)
            # clear the cart
            cart.clear()
            # launch asynchronous task
            # order_created.delay(order.id)
            return render(request,
                          'orders/order/created.html',
                          {'order': order})
    else:
        if request.user.is_authenticated:
            init_first_name = request.user.first_name
            init_last_name = request.user.last_name
            init_email = request.user.email
            user_profile = Profile.objects.get(user=request.user)
            init_phone = user_profile.phone
            init_city = user_profile.city
            init_address = user_profile.address
            init_postal_code = user_profile.postal_code
            form = OrderCreateForm(initial={'first_name': init_first_name,
                                            'last_name': init_last_name,
                                            'phone': init_phone,
                                            'email': init_email,
                                            'city': init_city,
                                            'address': init_address,
                                            'postal_code': init_postal_code})
        else:
            form = OrderCreateForm()

    return render(request,
                  'orders/order/create.html',
                  {'cart': cart, 'form': form})
