from django.conf import settings
from shop.models import ProductVariation


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, variation, quantity=1):
        variation_id = str(variation.id)
        if variation_id not in self.cart:
            self.cart[variation_id] = {'quantity': 0, 'price': variation.price}
        self.cart[variation_id]['quantity'] += quantity
        self.save()

    def remove(self, variation):
        variation_id = str(variation.id)
        if variation_id in self.cart:
            del self.cart[variation_id]
            self.save()

    def __iter__(self):
        variation_ids = self.cart.keys()
        variations = ProductVariation.objects.filter(id__in=variation_ids)
        cart = self.cart.copy()
        for variation in variations:
            cart[str(variation.id)]['variation'] = variation

        for item in cart.values():
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(item['price'] * item['quantity'] for item in self.cart.values())

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def save(self):
        self.session.modified = True
