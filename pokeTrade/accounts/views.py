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
            # Create UserProfile
            UserProfile.objects.create(
                user=user,
                birth_date=form.cleaned_data['birth_date'],
                gender=form.cleaned_data['gender']
            )
            login(request, user)
            return redirect('accounts:profile')  # Redirect to profile page after registration
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def profile(request):
    user_profile = request.user.userprofile
    return render(request, 'accounts/profile.html', {
        'profile': user_profile
    })

@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_profile = request.user.userprofile
        user_profile.bio = request.POST.get('bio', '')
        user_profile.location = request.POST.get('location', '')
        user_profile.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('accounts:profile')
    return render(request, 'accounts/edit_profile.html') 