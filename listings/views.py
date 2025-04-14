from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Listing
from offers.models import Offer
from .forms import ListingForm
import uuid

def listing_list(request):
    query = request.GET.get('q', '')
    sort = request.GET.get('sort', 'price_asc')
    listings = Listing.objects.filter(
        Q(name__icontains=query) if query else Q(),
        status='active'
    )

    if sort == 'price_asc':
        listings = listings.order_by('price')
    elif sort == 'price_desc':
        listings = listings.order_by('-price')

    return render(request, 'listings/listings_list.html', {
        'listings': listings,
        'query': query,
        'sort': sort
    })

def listing_detail(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, "Please log in to make an offer.")
            return redirect('login')
        if request.user == listing.seller:
            messages.error(request, "You cannot make an offer on your own listing.")
            return redirect('listing_detail', listing_id=listing_id)
        try:
            amount = float(request.POST.get('amount'))
            if amount <= 0:
                raise ValueError("Offer amount must be positive.")
            Offer.objects.create(
                listing=listing,
                buyer=request.user,
                amount=amount,
                status='pending'
            )
            messages.success(request, "Offer submitted successfully!")
            return redirect('listing_detail', listing_id=listing_id)
        except (ValueError, TypeError):
            messages.error(request, "Invalid offer amount.")
    return render(request, 'listings/listing_detail.html', {'listing': listing})

@login_required
def create_listing(request):
    if request.method == 'POST':
        form = ListingForm(request.POST)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.seller = request.user
            listing.status = 'active'
            # Generate unique card_id
            listing.card_id = f"user-{uuid.uuid4().hex[:10]}"
            listing.save()
            messages.success(request, "Listing created successfully!")
            return redirect('listing_list')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ListingForm()
    return render(request, 'listings/create_listing.html', {'form': form})
