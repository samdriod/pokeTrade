from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import UserProfile
from listings.models import Listing
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

class RegisterViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_register_view_post(self):
        response = self.client.post(reverse('accounts:register'), {
            'username': 'newuser',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
            'birth_date': '2000-01-01',
            'gender': 'M'
        })
        self.assertEqual(response.status_code, 302)  
        self.assertTrue(User.objects.filter(username='newuser').exists())
        self.assertTrue(UserProfile.objects.filter(user__username='newuser').exists())

class ProfileViewTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpass')

        # Create some Listing objects
        self.card1 = Listing.objects.create(
            card_id="xy1-1",
            name="Venusaur-EX",
            price=Decimal('500.00'),
            image="https://images.pokemontcg.io/xy1/1.png",
            condition="Mint",
            seller=self.user,
            status="active"
        )
        self.card2 = Listing.objects.create(
            card_id="xy1-2",
            name="Weedle",
            price=Decimal('20.00'),
            image="https://images.pokemontcg.io/xy1/2.png",
            condition="Near Mint",
            seller=self.user,
            status="pending"
        )

    def test_listing_recorded_in_database(self):
        # Check if the listing is recorded in the database
        listing = Listing.objects.filter(card_id="xy1-1", seller=self.user).exists()
        self.assertTrue(listing)

    def test_offer_recorded_in_database(self):
        # Check if the offer is recorded in the database
        offer = Listing.objects.filter(card_id="xy1-2", seller=self.user).exists()
        self.assertTrue(offer)

class EditProfileViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = Client()
        self.client.login(username='testuser', password='testpass')

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
        self.client.login(username='testuser', password='testpass')
        self.card1 = Listing.objects.create(
            card_id="xy1-1",
            name="Venusaur-EX",
            price=Decimal('500.00'),
            image="https://images.pokemontcg.io/xy1/1.png",
            condition="Mint",
            seller=self.user,
            status="active"
        )
        self.card2 = Listing.objects.create(
            card_id="xy1-2",
            name="M Venusaur-EX",
            price=Decimal('20.00'),
            image="https://images.pokemontcg.io/xy1/2.png",
            condition="Near Mint",
            seller=self.user,
            status="pending"
        )

    def test_pokemon_cards_recorded_in_database(self):
        # Check if the cards are recorded in the database
        card1_exists = Listing.objects.filter(card_id="xy1-1", name="Venusaur-EX").exists()
        card2_exists = Listing.objects.filter(card_id="xy1-2", name="M Venusaur-EX").exists()
        self.assertTrue(card1_exists)
        self.assertTrue(card2_exists)