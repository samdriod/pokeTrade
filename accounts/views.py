from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import UserProfile, PokemonCard
from .forms import CustomUserCreationForm, UserProfileForm

def register(request):
    if request.user.is_authenticated:
        return redirect('accounts:profile')
        
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            try:
                # Create the user first
                user = form.save()
                
                # Get or create the profile
                profile, created = UserProfile.objects.get_or_create(user=user)
                
                # Update profile fields from form
                profile.birth_date = form.cleaned_data.get('birth_date')
                profile.gender = form.cleaned_data.get('gender')
                if form.cleaned_data.get('email'):
                    user.email = form.cleaned_data.get('email')
                    user.save()
                
                # Save the profile
                profile.save()
                
                # Log the user in
                login(request, user)
                messages.success(request, 'Account created successfully!')
                return redirect('accounts:profile')
            except Exception as e:
                messages.error(request, f'Error creating account: {str(e)}')
        else:
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'accounts/register.html', {'form': form})

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

@login_required
def pokedex(request):
    cards = PokemonCard.objects.all()
    
    # Handle search query
    search_query = request.GET.get('search', '')
    if search_query:
        cards = cards.filter(name__icontains=search_query)
    
    # Handle filters
    rarity = request.GET.get('rarity', '')
    if rarity:
        cards = cards.filter(rarity=rarity)
        
    type_filter = request.GET.get('type', '')
    if type_filter:
        cards = cards.filter(supertype=type_filter)
    
    # Get unique values for filter dropdowns
    rarities = PokemonCard.objects.values_list('rarity', flat=True).distinct()
    types = PokemonCard.objects.values_list('supertype', flat=True).distinct()
    
    context = {
        'cards': cards,
        'search_query': search_query,
        'selected_rarity': rarity,
        'selected_type': type_filter,
        'rarities': rarities,
        'types': types,
    }
    
    return render(request, 'accounts/pokedex.html', context) 