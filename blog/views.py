# blog/views.py

from django.contrib import messages
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from shop.models import Tag

from .forms import CommentForm
from .models import Post

POSTS_PER_PAGE = 6


def post_list(request):
    """Published post list with search (q=) and tag (tag=) filtering."""
    queryset = (
        Post.objects.filter(status="published")
        .select_related("author")
        .prefetch_related("tags")
    )

    query = request.GET.get("q", "").strip()
    tag_slug = request.GET.get("tag", "").strip()
    current_tag = None

    if query:
        queryset = queryset.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )

    if tag_slug:
        current_tag = get_object_or_404(Tag, slug=tag_slug)
        queryset = queryset.filter(tags=current_tag)

    paginator = Paginator(queryset, POSTS_PER_PAGE)
    page_number = request.GET.get("page")
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    # Only tags that appear on at least one published post
    all_tags = Tag.objects.filter(blog_posts__status="published").distinct()

    context = {
        "page_obj": page_obj,
        "query": query,
        "current_tag": current_tag,
        "all_tags": all_tags,
    }
    return render(request, "blog/post_list.html", context)


def post_detail(request, slug):
    """Single post view with related posts and comment handling."""
    post = get_object_or_404(Post, slug=slug, status="published")
    comments = post.comments.filter(is_active=True)

    # Related posts: share at least one tag, exclude self, cap at 3
    post_tag_ids = post.tags.values_list("id", flat=True)
    related_posts = (
        Post.objects.filter(status="published", tags__in=post_tag_ids)
        .exclude(id=post.id)
        .distinct()[:3]
    )

    form = CommentForm()

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            if request.user.is_authenticated:
                comment.user = request.user
                comment.name = ""  # resolved via get_display_name()
            elif not comment.name:
                comment.name = "مهمان ناشناس"
            comment.save()
            messages.success(request, "نظر شما با موفقیت ثبت شد.")
            return redirect(post.get_absolute_url() + "#comments")

    context = {
        "post": post,
        "comments": comments,
        "form": form,
        "related_posts": related_posts,
    }
    return render(request, "blog/post_detail.html", context)
