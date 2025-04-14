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
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='', blank=True)
    reputation_score = models.IntegerField(default=0)
    trades_completed = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.nickname or self.user.username}'s profile"

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """Create or update a UserProfile instance when a User is saved."""
    if created:
        # For new users, create profile
        UserProfile.objects.create(user=instance)
    else:
        # For existing users, ensure profile exists
        UserProfile.objects.get_or_create(user=instance)
