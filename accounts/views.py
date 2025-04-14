from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

from offers.models import Offer
from .models import UserProfile
from .forms import CustomUserCreationForm, UserProfileForm
from django.db import transaction

def register(request):
    if request.user.is_authenticated:
        return redirect('accounts:profile')
        
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    # Create the user first
                    user = form.save()
                    
                    # Update the user's profile
                    profile = user.userprofile  # Profile is created by signal
                    profile.birth_date = form.cleaned_data.get('birth_date')
                    profile.gender = form.cleaned_data.get('gender')
                    profile.save()
                    
                    # Update email if provided
                    if form.cleaned_data.get('email'):
                        user.email = form.cleaned_data.get('email')
                        user.save()
                    
                    # Log the user in
                    login(request, user)
                    messages.success(request, 'Account created successfully!')
                    return redirect('accounts:profile')
            except Exception as e:
                # If anything goes wrong, make sure to delete the user if it was created
                if 'user' in locals():
                    user.delete()
                messages.error(request, f'Error creating account: {str(e)}')
        else:
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def profile(request):
    user_offers = Offer.objects.filter(buyer=request.user)
    return render(request, 'accounts/profile.html', {
        'profile': request.user.userprofile,
        'offers': user_offers
    })

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user.userprofile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('accounts:profile')
    else:
        form = UserProfileForm(instance=request.user.userprofile)
    
    return render(request, 'accounts/edit_profile.html', {'form': form})
