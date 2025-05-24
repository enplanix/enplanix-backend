from django.core.management.base import BaseCommand
from ...utils import generate_business_categories

class Command(BaseCommand):
    help = "Generate default categories if they don't exist."
    
    def handle(self, *args, **kwargs):
        generate_business_categories()
        self.stdout.write(self.style.SUCCESS('Default categories generated successfully.'))
