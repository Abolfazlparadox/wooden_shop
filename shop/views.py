from django.views.generic import ListView, DetailView
from django.shortcuts import render, redirect
from .models import Product, ProductVariation, Category, Review
from .forms import ReviewForm

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
        return super().get_queryset().prefetch_related(
            'variations__images', 'images', 'reviews__user'
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        
        # Inject related products
        context['related_products'] = Product.objects.filter(
            category=product.category, is_active=True
        ).exclude(pk=product.pk)[:4]
        
        # Inject reviews and review form
        context['reviews'] = product.reviews.all()
        context['review_form'] = ReviewForm()
        
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        review_form = ReviewForm(request.POST)

        if review_form.is_valid():
            if request.user.is_authenticated:
                new_review = review_form.save(commit=False)
                new_review.product = self.object
                new_review.user = request.user
                new_review.save()
                return redirect(self.object.get_absolute_url())
            else:
                # Handle case for non-authenticated users, e.g., redirect to login
                return redirect('login') # Assuming you have a login URL named 'login'

        # If form is not valid, re-render the page with the form and errors
        context = self.get_context_data(object=self.object, review_form=review_form)
        return self.render_to_response(context)
