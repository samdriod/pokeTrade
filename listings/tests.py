from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.core.management import call_command
from django.urls import reverse
from .models import Listing
import os
import json
from decimal import Decimal

class ListingModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.listing = Listing.objects.create(
            card_id='xy1-1',
            name='Venusaur-EX',
            price=10.50,
            image='http://example.com/image.jpg',
            condition='Mint',
            seller=self.user,
            status='active'
        )

    def test_listing_creation(self):
        self.assertEqual(self.listing.name, 'Venusaur-EX')
        self.assertEqual(self.listing.price, 10.50)
        self.assertEqual(self.listing.condition, 'Mint')
        self.assertEqual(self.listing.status, 'active')
        self.assertEqual(str(self.listing), 'Venusaur-EX (xy1-1)')

class LoadCardsCommandTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='demo_user', password='demo123')
        self.json_path = os.path.join(os.path.dirname(__file__), 'test_pokemon_cards.json')
        self.cards_data = [
            {
                "id": "xy1-1",
                "name": "Venusaur-EX",
                "tcgplayer": {"prices": {"holofoil": {"market": 3.52}}},
                "images": {"small": "https://images.pokemontcg.io/xy1/1.png"}
            }
        ]
        with open(self.json_path, 'w') as f:
            json.dump(self.cards_data, f)

    def tearDown(self):
        if os.path.exists(self.json_path):
            os.remove(self.json_path)

    def test_load_cards_command(self):
        call_command('load_cards')
        listing = Listing.objects.get(card_id='xy1-1')
        self.assertEqual(listing.name, 'Venusaur-EX')
        self.assertEqual(listing.price, Decimal('3.52'))  # Use Decimal for comparison
        self.assertEqual(listing.image, 'https://images.pokemontcg.io/xy1/1.png')  # Updated to match actual data
        self.assertEqual(listing.seller.username, 'demo_user')

class ListingListViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.listing = Listing.objects.create(
            card_id='xy1-1',
            name='Venusaur-EX',
            price=10.50,
            image='http://example.com/image.jpg',
            condition='Mint',
            seller=self.user,
            status='active'
        )

    def test_listing_list_view(self):
        response = self.client.get(reverse('listing_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Venusaur-EX')
        self.assertTemplateUsed(response, 'listings/listings_list.html')
