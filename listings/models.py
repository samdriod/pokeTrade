from django.db import models
from django.contrib.auth.models import User

class Listing(models.Model):
    card_id = models.CharField(max_length=50, unique=True)  # e.g., "xy1-1"
    name = models.CharField(max_length=100)               # e.g., "Venusaur-EX"
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Seller’s price
    image = models.URLField(blank=True)                  # API image URL
    condition = models.CharField(max_length=50, blank=True)  # e.g., "Mint"
    seller = models.ForeignKey(User, on_delete=models.CASCADE)  # Links to user
    status = models.CharField(max_length=20, default='active')  # active/sold
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.card_id})"