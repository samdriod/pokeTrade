from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import UserProfile, PokemonCard, CardListing

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'

class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

@admin.register(PokemonCard)
class PokemonCardAdmin(admin.ModelAdmin):
    list_display = ('name', 'set_name', 'rarity', 'supertype')
    list_filter = ('supertype', 'rarity', 'set_name')
    search_fields = ('name', 'card_id')
    ordering = ('name',)

@admin.register(CardListing)
class CardListingAdmin(admin.ModelAdmin):
    list_display = ('card', 'seller', 'price', 'condition', 'status')
    list_filter = ('status', 'condition', 'is_foil')
    search_fields = ('card__name', 'seller__username', 'description')
    ordering = ('-created_at',) 