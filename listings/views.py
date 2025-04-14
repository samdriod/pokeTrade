from django.shortcuts import render
from .models import Listing

def listing_list(request):
    listings = Listing.objects.filter(status='active').order_by('name')
    return render(request, 'listings/listings_list.html', {'listings': listings})
