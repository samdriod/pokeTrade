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
        help_text='Optional. This will be displayed instead of your username.'
    )
    
    class Meta:
        model = UserProfile
        fields = ('nickname', 'birth_date', 'gender', 'location', 'bio')
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        } 