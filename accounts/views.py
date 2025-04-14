from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import UserProfile
from .forms import CustomUserCreationForm, UserProfileForm

def register(request):
    if request.user.is_authenticated:
        return redirect('accounts:profile')  # Add namespace
        
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Update the automatically created profile
            user.userprofile.birth_date = form.cleaned_data['birth_date']
            user.userprofile.gender = form.cleaned_data['gender']
            user.userprofile.save()
            login(request, user)
            return redirect('accounts:profile')  # Add namespace
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def profile(request):
    return render(request, 'accounts/profile.html', {
        'profile': request.user.userprofile
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