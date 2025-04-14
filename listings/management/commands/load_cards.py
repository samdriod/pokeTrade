from django.core.management.base import BaseCommand
from listings.models import Listing
from django.contrib.auth.models import User
import json
import os


class Command(BaseCommand):
    help = 'Load Pokémon cards from JSON into database'

    def handle(self, *args, **kwargs):
        # Path to pokemon_cards_clean.json in project root
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
        json_path = os.path.join(project_root, 'pokemon_cards_clean.json')

        # Create or get a demo user
        demo_user, _ = User.objects.get_or_create(username='demo_user', defaults={'password': 'demo123'})

        try:
            with open(json_path, 'r') as f:
                cards = json.load(f)

            for card in cards:
                Listing.objects.get_or_create(
                    card_id=card['id'],
                    defaults={
                        'name': card['name'],
                        'price': card.get('tcgplayer', {}).get('prices', {}).get('holofoil', {}).get('market',
                                                                                                     0.0) or 0.0,
                        'image': card.get('images', {}).get('small', ''),
                        'condition': 'Unknown',  # Default for API data
                        'seller': demo_user,
                        'status': 'active',
                    }
                )
            self.stdout.write(self.style.SUCCESS(f'Loaded {len(cards)} cards into database'))
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'pokemon_cards_clean.json not found at {json_path}'))
        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR('Invalid JSON format'))