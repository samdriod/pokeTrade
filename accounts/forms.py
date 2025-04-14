from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile

class CustomUserCreationForm(UserCreationForm):
    GENDER_CHOICES = [
        ('', 'Prefer not to say'),
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    ]
    
    birth_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        help_text='Required. Please enter your birth date.'
    )
    gender = forms.ChoiceField(
        choices=GENDER_CHOICES,
        required=False,
        help_text='Optional. Select your gender.'
    )
    email = forms.EmailField(
        required=False,
        help_text='Optional. Enter a valid email address.'
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'birth_date', 'gender', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = 'Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'
        self.fields['password1'].help_text = 'Your password must contain at least 8 characters.'

class UserProfileForm(forms.ModelForm):
    nickname = forms.CharField(
        max_length=30,
        required=False,
        help_text='Optional. This will be displayed instead of your username.',
        widget=forms.TextInput(attrs={
            'class': 'mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'
        })
    )
    
    class Meta:
        model = UserProfile
        fields = ('nickname', 'birth_date', 'gender', 'location', 'bio')
        widgets = {
            'birth_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'
            }),
            'gender': forms.Select(attrs={
                'class': 'mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
            }),
            'location': forms.TextInput(attrs={
                'class': 'mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'
            }),
            'bio': forms.Textarea(attrs={
                'rows': 3,
                'class': 'mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'
            })
        } 