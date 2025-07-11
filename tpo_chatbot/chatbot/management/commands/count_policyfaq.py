from django.core.management.base import BaseCommand
from chatbot.models import PolicyFAQ

class Command(BaseCommand):
    help = 'Counts the number of entries in the PolicyFAQ model.'

    def handle(self, *args, **kwargs):
        # Count the number of entries in the PolicyFAQ model
        count = PolicyFAQ.objects.count()
        
        # Output the count
        self.stdout.write(self.style.SUCCESS(f'There are {count} entries in the PolicyFAQ model.'))