from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from shop.models import ProductVariation
from .cart import Cart
from .forms import OrderCreateForm
from .models import OrderItem


@require_POST
def cart_add(request, variation_id):
    cart = Cart(request)
    variation = get_object_or_404(ProductVariation, id=variation_id)
    # You might want to add form validation for quantity here
    quantity = int(request.POST.get('quantity', 1))
    cart.add(variation=variation, quantity=quantity)
    return redirect('orders:cart_detail')


@require_POST
def cart_remove(request, variation_id):
    cart = Cart(request)
    variation = get_object_or_404(ProductVariation, id=variation_id)
    cart.remove(variation)
    return redirect('orders:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'orders/cart_detail.html', {'cart': cart})


def checkout(request):
    cart = Cart(request)
    if len(cart) == 0:
        return redirect('shop:product_list')

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user
            order.total_price = cart.get_total_price()
            order.save()

            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    variation=item['variation'],
                    price=item['price'],
                    quantity=item['quantity']
                )
            
            cart.clear()
            
            # For now, redirect to a simple success message or page
            # You can create a proper order success page later
            return render(request, 'orders/order_created.html', {'order': order})
    else:
        form = OrderCreateForm()

    return render(request, 'orders/checkout.html', {'cart': cart, 'form': form})
