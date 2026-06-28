# blog/forms.py

from django import forms

from .models import Comment

# Shared Tailwind class string for all text inputs — matches the site's design system
_INPUT = (
    "w-full rounded-xl px-4 py-3 "
    "bg-white dark:bg-slate-700 "
    "border border-slate-200 dark:border-slate-600 "
    "focus:ring-2 focus:ring-walnut-800 focus:border-transparent "
    "outline-none transition-all duration-200 "
    "text-slate-800 dark:text-slate-100 "
    "placeholder-slate-400 dark:placeholder-slate-500 "
    "text-sm"
)

_TEXTAREA = _INPUT + " resize-none"


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["name", "body"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": _INPUT,
                    "placeholder": "نام شما",
                    "autocomplete": "name",
                    "dir": "rtl",
                }
            ),
            "body": forms.Textarea(
                attrs={
                    "class": _TEXTAREA,
                    "placeholder": "نظر خود را اینجا بنویسید...",
                    "rows": 5,
                    "dir": "rtl",
                }
            ),
        }
        labels = {
            "name": "نام",
            "body": "متن نظر",
        }
        error_messages = {
            "body": {"required": "لطفاً متن نظر را وارد کنید."},
        }
