from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from shop.models import ProductVariation
from .cart import Cart


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
    # A simple JSON response for now, as requested.
    # In a real scenario, you would render a template.
    cart_items = []
    for item in cart:
        cart_items.append({
            'variation_id': item['variation'].id,
            'sku': item['variation'].sku,
            'quantity': item['quantity'],
            'price': item['price'],
            'total_price': item['total_price'],
        })
    return JsonResponse({
        'items': cart_items,
        'total_price': cart.get_total_price(),
        'total_items': len(cart)
    })
    # Or render a template:
    # return render(request, 'orders/cart.html', {'cart': cart})
