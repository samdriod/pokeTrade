from django.db import models
from django.contrib.auth.models import User
from listings.models import Listing

class Offer(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='offers')
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='offers_made')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default='pending', choices=[
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined')
    ])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"${self.amount} offer on {self.listing.name} by {self.buyer.username}"

    class Meta:
        ordering = ['-created_at']
