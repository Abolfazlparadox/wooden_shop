from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-walnut-800 focus:ring-walnut-800 sm:text-sm dark:bg-slate-800 dark:border-slate-600'
            }),
            'comment': forms.Textarea(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-walnut-800 focus:ring-walnut-800 sm:text-sm dark:bg-slate-800 dark:border-slate-600',
                'rows': 4,
                'placeholder': 'نظر خود را بنویسید...'
            }),
        }
