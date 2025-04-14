from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import UserProfile, PokemonCard, CardListing
from django.urls import reverse
from datetime import date
from decimal import Decimal

class UserProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.profile = UserProfile.objects.get(user=self.user)
        self.profile.nickname = "Test Nickname"
        self.profile.birth_date = date(2000, 1, 1)
        self.profile.gender = "M"
        self.profile.save()

    def test_user_profile_creation(self):
        self.assertEqual(self.profile.nickname, "Test Nickname")
        self.assertEqual(self.profile.birth_date, date(2000, 1, 1))
        self.assertEqual(self.profile.gender, "M")
        self.assertEqual(str(self.profile), "Test Nickname's profile")

class PokemonCardModelTest(TestCase):
    def setUp(self):
        self.card = PokemonCard.objects.create(
            card_id="xy1-1",
            name="Venusaur-EX",
            supertype="Pokémon",
            subtypes=["EX"],
            hp="180",
            types=["Grass"],
            number="1",
            artist="Eske Yoshinob",
            rarity="Rare Holo EX",
            set_name="XY",
            set_series="XY",
            small_image="https://images.pokemontcg.io/xy1/1.png",
            large_image="https://images.pokemontcg.io/xy1/1_hires.png",
            tcgplayer_url="https://prices.pokemontcg.io/tcgplayer/xy1-1",
            cardmarket_url="https://prices.pokemontcg.io/cardmarket/xy1-1"
        )

    def test_pokemon_card_creation(self):
        self.assertEqual(self.card.name, "Venusaur-EX")
        self.assertEqual(self.card.supertype, "Pokémon")
        self.assertEqual(self.card.rarity, "Rare Holo EX")
        self.assertEqual(str(self.card), "Venusaur-EX (XY 1)")

class RegisterViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_register_view_get(self):
        response = self.client.get(reverse('accounts:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/register.html')

    def test_register_view_post(self):
        response = self.client.post(reverse('accounts:register'), {
            'username': 'newuser',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
            'birth_date': '2000-01-01',
            'gender': 'M'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful registration
        self.assertTrue(User.objects.filter(username='newuser').exists())
        self.assertTrue(UserProfile.objects.filter(user__username='newuser').exists())

class ProfileViewTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpass')

        # Create some PokemonCard objects
        self.card1 = PokemonCard.objects.create(
            card_id="xy1-1",
            name="Venusaur-EX",
            supertype="Pokémon",
            rarity="Rare Holo EX",
            set_name="XY",
            set_series="XY",
            small_image="https://images.pokemontcg.io/xy1/1.png"
        )
        self.card2 = PokemonCard.objects.create(
            card_id="xy1-2",
            name="Weedle",
            supertype="Pokémon",
            rarity="Common",
            set_name="XY",
            set_series="XY",
            small_image="https://images.pokemontcg.io/xy1/2.png"
        )

        # Create a listing for the user
        self.listing = CardListing.objects.create(
            seller=self.user,
            card=self.card1,
            condition="MT",
            price=Decimal('500.00'),
            description="Mint condition Venusaur-EX",
            status="available"
        )

        # Create an offer for the user
        self.offer = CardListing.objects.create(
            seller=self.user,
            card=self.card2,
            condition="NM",
            price=Decimal('20.00'),
            description="Near Mint Weedle",
            status="pending"
        )

    def test_listing_recorded_in_database(self):
        # Check if the listing is recorded in the database
        listing = CardListing.objects.filter(card=self.card1, seller=self.user).exists()
        self.assertTrue(listing)

    def test_offer_recorded_in_database(self):
        # Check if the offer is recorded in the database
        offer = CardListing.objects.filter(card=self.card2, seller=self.user).exists()
        self.assertTrue(offer)

class EditProfileViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = Client()
        self.client.login(username='testuser', password='testpass')

    def test_edit_profile_view_get(self):
        response = self.client.get(reverse('accounts:edit_profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/edit_profile.html')

    def test_edit_profile_view_post(self):
        response = self.client.post(reverse('accounts:edit_profile'), {
            'nickname': 'Updated Nickname',
            'birth_date': '1995-05-15',
            'gender': 'F',
            'location': 'Test Location',
            'bio': 'Updated bio'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful update
        profile = UserProfile.objects.get(user=self.user)
        self.assertEqual(profile.nickname, 'Updated Nickname')
        self.assertEqual(profile.birth_date, date(1995, 5, 15))
        self.assertEqual(profile.gender, 'F')
        self.assertEqual(profile.location, 'Test Location')
        self.assertEqual(profile.bio, 'Updated bio')

class PokedexViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')  # Log in the test client
        self.card1 = PokemonCard.objects.create(
            card_id="xy1-1",
            name="Venusaur-EX",
            supertype="Pokémon",
            rarity="Rare Holo EX",
            small_image="https://images.pokemontcg.io/xy1/1.png"
        )
        self.card2 = PokemonCard.objects.create(
            card_id="xy1-2",
            name="M Venusaur-EX",
            supertype="Pokémon",
            rarity="Rare Holo EX",
            small_image="https://images.pokemontcg.io/xy1/2.png"
        )

    def test_pokedex_view(self):
        response = self.client.get(reverse('accounts:pokedex'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/pokedex.html')
        self.assertContains(response, 'Venusaur-EX')
        self.assertContains(response, 'M Venusaur-EX')

    def test_pokemon_cards_recorded_in_database(self):
        # Check if the cards are recorded in the database
        card1_exists = PokemonCard.objects.filter(card_id="xy1-1", name="Venusaur-EX").exists()
        card2_exists = PokemonCard.objects.filter(card_id="xy1-2", name="M Venusaur-EX").exists()
        self.assertTrue(card1_exists)
        self.assertTrue(card2_exists)