from django import forms
from .models import Listing

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['name', 'price', 'condition', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'border rounded p-2 w-full', 'placeholder': 'e.g., Pikachu'}),
            'price': forms.NumberInput(attrs={'class': 'border rounded p-2 w-full', 'step': '0.01', 'min': '0.01', 'placeholder': 'e.g., 5.00'}),
            'condition': forms.TextInput(attrs={'class': 'border rounded p-2 w-full', 'placeholder': 'e.g., Mint'}),
            'image': forms.URLInput(attrs={'class': 'border rounded p-2 w-full', 'placeholder': 'Optional image URL'}),
        }
        labels = {
            'name': 'Card Name',
            'price': 'Asking Price ($)',
            'condition': 'Condition',
            'image': 'Image URL (optional)',
        }
