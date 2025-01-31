from django.core.management.base import BaseCommand
from chatbot.models import PolicyFAQ
class Command(BaseCommand):
    help = 'Clear all data from PolicyFAQ model'

    def handle(self, *args, **kwargs):
        deleted_count, _ = PolicyFAQ.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f'Successfully deleted {deleted_count} records from PolicyFAQ.'))