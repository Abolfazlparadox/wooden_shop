# shop/context_processors.py
from .models import Category

def categories_processor(request):
    """
    Makes all Category objects available to all templates.
    """
    # This simplified version works whether or not a parent/child relationship exists.
    # The template is already designed to handle both cases gracefully.
    return {'menu_categories': Category.objects.all()}
