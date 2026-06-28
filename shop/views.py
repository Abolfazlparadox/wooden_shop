from django.core.paginator import Paginator
from django.db.models import Prefetch, Q
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.generic import DetailView

from .forms import ReviewForm
from .models import Category, Product, Review

# shop/views.py


def search_suggestions_api(request):
    """
    API endpoint for live search suggestions.
    """
    query = request.GET.get("q", "").strip()

    # Return empty if query is too short
    if len(query) < 2:
        return JsonResponse({"suggestions": []})

    # Query products by title, slug, and tags
    products = (
        Product.objects.filter(
            Q(title__icontains=query)
            | Q(slug__icontains=query)
            | Q(tags__name__icontains=query)
        )
        .distinct()
        .select_related("category")[:4]
    )  # Limit to 4 results and optimize category query

    suggestions = [
        {
            "title": p.title,
            "url": p.get_absolute_url(),
            "category": p.category.name if p.category else "",
        }
        for p in products
    ]

    return JsonResponse({"suggestions": suggestions})


def home_page(request):
    categories = Category.objects.all()
    featured_products = Product.objects.filter(is_active=True).order_by("-created_at")[
        :8
    ]
    context = {
        "categories": categories,
        "featured_products": featured_products,
    }
    return render(request, "shop/home.html", context)


def product_list(request):
    products = Product.objects.filter(is_active=True)

    # Search
    query = request.GET.get("q")
    if query:
        products = products.filter(
            Q(title__icontains=query)
            | Q(description__icontains=query)
            | Q(tags__name__icontains=query)
        )

    # Filtering
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")
    in_stock = request.GET.get("in_stock")
    special_sale = request.GET.get("special_sale")

    if min_price:
        products = products.filter(variations__price__gte=min_price)
    if max_price:
        products = products.filter(variations__price__lte=max_price)
    if in_stock:
        products = products.filter(variations__stock__gt=0)
    if special_sale:
        products = products.filter(variations__discount_price__isnull=False)

    # Sorting
    sort_by = request.GET.get("sort", "default")
    if sort_by == "price_asc":
        products = products.order_by("variations__price")
    elif sort_by == "price_desc":
        products = products.order_by("-variations__price")
    elif sort_by == "newest":
        products = products.order_by("-created_at")
    else:  # default
        products = products.order_by("-created_at")

    products = products.distinct()

    # Pagination
    paginator = Paginator(products, 9)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "products": page_obj,
        "page_obj": page_obj,
        "paginator": paginator,
        "sort_by": sort_by,
        "values": request.GET,
    }
    return render(request, "shop/product_list.html", context)


class ProductDetailView(DetailView):
    model = Product
    template_name = "shop/product_detail.html"
    context_object_name = "product"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        return super().get_queryset().prefetch_related("variations__images", "images")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()

        context["related_products"] = Product.objects.filter(
            category=product.category, is_active=True
        ).exclude(pk=product.pk)[:4]

        context["reviews"] = (
            product.reviews.filter(is_approved=True, parent__isnull=True)
            .select_related("user")
            .prefetch_related(
                Prefetch(
                    "replies",
                    queryset=Review.objects.filter(is_approved=True).select_related(
                        "user"
                    ),
                )
            )
        )
        context["review_form"] = ReviewForm()

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
                return redirect("accounts:login")

        context = self.get_context_data(object=self.object, review_form=review_form)
        return self.render_to_response(context)
