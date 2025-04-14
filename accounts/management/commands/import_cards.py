import json
from django.core.management.base import BaseCommand
from pokeTrade.accounts.models import PokemonCard

class Command(BaseCommand):
    help = 'Import Pokemon cards from JSON file'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='Path to the JSON file containing Pokemon card data')

    def handle(self, *args, **options):
        json_file = options['json_file']
        
        try:
            with open(json_file, 'r', encoding='utf-8') as file:
                cards_data = json.load(file)
                
            cards_created = 0
            cards_updated = 0
            
            for card_entry in cards_data:
                card_data = card_entry.get('data', {})
                if not card_data:
                    continue
                
                # Extract set information
                set_info = card_data.get('set', {})
                
                # Extract image URLs
                images = card_data.get('images', {})
                
                # Create or update card
                card, created = PokemonCard.objects.update_or_create(
                    card_id=card_data.get('id'),
                    defaults={
                        'name': card_data.get('name', ''),
                        'supertype': card_data.get('supertype', ''),
                        'subtypes': card_data.get('subtypes', []),
                        'hp': card_data.get('hp', ''),
                        'types': card_data.get('types', []),
                        'number': card_data.get('number', ''),
                        'artist': card_data.get('artist', ''),
                        'rarity': card_data.get('rarity', ''),
                        'set_name': set_info.get('name', ''),
                        'set_series': set_info.get('series', ''),
                        'small_image': images.get('small', ''),
                        'large_image': images.get('large', ''),
                        'tcgplayer_url': card_data.get('tcgplayer', {}).get('url', ''),
                        'cardmarket_url': card_data.get('cardmarket', {}).get('url', '')
                    }
                )
                
                if created:
                    cards_created += 1
                else:
                    cards_updated += 1
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully imported cards: {cards_created} created, {cards_updated} updated'
                )
            )
            
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'File not found: {json_file}'))
        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR('Invalid JSON file'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error importing cards: {str(e)}')) 