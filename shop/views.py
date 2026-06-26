from django.views.generic import ListView, DetailView
from .models import Product, ProductVariation, Category, Review


class ProductListView(ListView):
    model = Product
    template_name = 'shop/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.filter(is_active=True).order_by('-created_at')


class ProductDetailView(DetailView):
    model = Product
    template_name = 'shop/product_detail.html'
    context_object_name = 'product'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        # Prefetch related data to prevent N+1 queries
        return super().get_queryset().prefetch_related(
            'variations',
            'images',
            'reviews__user'
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()

        context['variations'] = product.variations.all()
        context['images'] = product.images.all()
        # FIX: Removed the filter for the non-existent 'is_active' field
        context['reviews'] = product.reviews.all()

        return context
