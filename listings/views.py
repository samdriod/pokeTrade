from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Listing

def listing_list(request):
    listings = Listing.objects.filter(status='active').order_by('name')
    return render(request, 'listings/listings_list.html', {'listings': listings})

def listing_detail(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    return render(request, 'listings/listing_detail.html', {'listing': listing})