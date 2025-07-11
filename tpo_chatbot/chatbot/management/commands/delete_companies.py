from django.core.management.base import BaseCommand
from chatbot.models import CompanyInfo

class Command(BaseCommand):
    help = "Deletes all entries from the CompanyInfo model"

    def handle(self, *args, **kwargs):
        count = CompanyInfo.objects.count()
        CompanyInfo.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f"Deleted {count} company records."))
