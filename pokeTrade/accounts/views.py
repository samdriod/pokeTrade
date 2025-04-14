from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import UserProfile
from .forms import CustomUserCreationForm

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Update the automatically created profile
            user.userprofile.birth_date = form.cleaned_data['birth_date']
            user.userprofile.gender = form.cleaned_data['gender']
            user.userprofile.save()
            login(request, user)
            return redirect('accounts:profile')
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
        user = request.user
        profile = user.userprofile

        # Update user email
        user.email = request.POST.get('email', '')
        user.save()

        # Update profile fields
        profile.birth_date = request.POST.get('birth_date') or None
        profile.gender = request.POST.get('gender', '')
        profile.location = request.POST.get('location', '')
        profile.bio = request.POST.get('bio', '')
        profile.save()

        messages.success(request, 'Profile updated successfully!')
        return redirect('accounts:profile')

    return render(request, 'accounts/edit_profile.html', {
        'profile': request.user.userprofile
    }) 