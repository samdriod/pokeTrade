from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    GENDER_CHOICES = [
        ('', 'Prefer not to say'),
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=30, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    reputation_score = models.IntegerField(default=0)
    trades_completed = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.nickname or self.user.username}'s profile"

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """Create or update a UserProfile instance when a User is saved."""
    if created:
        # Create new profile
        UserProfile.objects.create(
            user=instance,
            birth_date=getattr(instance, '_birth_date', None),
            gender=getattr(instance, '_gender', '')
        )
    elif hasattr(instance, '_birth_date'):
        # Update existing profile
        profile = instance.userprofile
        profile.birth_date = instance._birth_date
        profile.gender = instance._gender
        profile.save()

class PokemonCard(models.Model):
    # Card identification
    card_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    supertype = models.CharField(max_length=50)
    subtypes = models.JSONField(default=list)
    hp = models.CharField(max_length=10, null=True, blank=True)
    types = models.JSONField(default=list)
    
    # Card details
    number = models.CharField(max_length=20)
    artist = models.CharField(max_length=100, null=True, blank=True)
    rarity = models.CharField(max_length=50, null=True, blank=True)
    set_name = models.CharField(max_length=100)
    set_series = models.CharField(max_length=100)
    
    # Card images
    small_image = models.URLField(max_length=500)
    large_image = models.URLField(max_length=500)
    
    # Market data
    tcgplayer_url = models.URLField(max_length=500, null=True, blank=True)
    cardmarket_url = models.URLField(max_length=500, null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.set_name} {self.number})"

    class Meta:
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['set_name']),
            models.Index(fields=['rarity']),
        ]

class CardListing(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('pending', 'Trade Pending'),
        ('completed', 'Trade Completed'),
        ('cancelled', 'Cancelled')
    ]
    
    CONDITION_CHOICES = [
        ('MT', 'Mint'),
        ('NM', 'Near Mint'),
        ('EX', 'Excellent'),
        ('GD', 'Good'),
        ('LP', 'Lightly Played'),
        ('PL', 'Played'),
        ('PR', 'Poor')
    ]

    # Listing details
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings')
    card = models.ForeignKey(PokemonCard, on_delete=models.CASCADE)
    condition = models.CharField(max_length=2, choices=CONDITION_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    is_foil = models.BooleanField(default=False)
    
    # Trading preferences
    willing_to_trade = models.BooleanField(default=True)
    cards_wanted = models.ManyToManyField(PokemonCard, related_name='wanted_in_listings', blank=True)
    
    # Listing status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.card.name} - {self.get_condition_display()} - ${self.price}"

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['condition']),
            models.Index(fields=['-created_at']),
        ] 