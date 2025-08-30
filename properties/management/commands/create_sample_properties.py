from django.core.management.base import BaseCommand
from properties.models import Property
from decimal import Decimal
import random


class Command(BaseCommand):
    help = 'Create sample properties for testing caching functionality'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=50,
            help='Number of sample properties to create (default: 50)',
        )

    def handle(self, *args, **options):
        count = options['count']
        
        # Sample data
        titles = [
            'Modern Downtown Apartment', 'Suburban Family Home', 'Luxury Waterfront Villa',
            'Cozy Studio Apartment', 'Spacious Townhouse', 'Historic Victorian House',
            'Contemporary Loft', 'Beachfront Condo', 'Mountain Cabin Retreat',
            'Urban Penthouse', 'Charming Cottage', 'Executive Office Building',
        ]
        
        locations = [
            'New York, NY', 'Los Angeles, CA', 'Chicago, IL', 'Houston, TX',
            'Phoenix, AZ', 'Philadelphia, PA', 'San Antonio, TX', 'San Diego, CA',
            'Dallas, TX', 'San Jose, CA', 'Austin, TX', 'Jacksonville, FL',
        ]
        
        descriptions = [
            'Beautiful property with modern amenities and stunning views.',
            'Perfect for families, featuring spacious rooms and a large yard.',
            'Luxury living with premium finishes and excellent location.',
            'Ideal investment opportunity in a growing neighborhood.',
            'Recently renovated with top-of-the-line appliances.',
            'Quiet and peaceful setting with easy access to city center.',
        ]

        # Create sample properties
        created_count = 0
        for i in range(count):
            try:
                property_obj = Property.objects.create(
                    title=f"{random.choice(titles)} #{i+1}",
                    description=random.choice(descriptions),
                    price=Decimal(str(random.randint(100000, 2000000))),
                    location=random.choice(locations),
                )
                created_count += 1
                
                if created_count % 10 == 0:
                    self.stdout.write(f'Created {created_count}/{count} properties...')
                    
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Error creating property: {e}')
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {created_count} sample properties!'
            )
        )