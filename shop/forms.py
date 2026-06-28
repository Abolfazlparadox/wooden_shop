from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']

        attrs_dict = {
            'class': 'w-full px-4 py-3 rounded-xl border border-slate-200 bg-slate-50 text-slate-800 focus:outline-none focus:ring-2 focus:ring-walnut-800 focus:border-transparent transition-all duration-300 dark:bg-slate-800 dark:border-slate-700 dark:text-white dark:focus:ring-walnut-500'
        }

        widgets = {
            'rating': forms.Select(attrs=attrs_dict),
            'comment': forms.Textarea(attrs={**attrs_dict, 'rows': 4, 'placeholder': 'نظر خود را بنویسید...'}),
        }
