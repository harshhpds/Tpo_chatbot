import csv
from django.core.management.base import BaseCommand
from chatbot.models import PolicyFAQ

class Command(BaseCommand):
    help = "Export PolicyFAQ model data to a CSV file"

    def handle(self, *args, **kwargs):
        file_path = "policy_faqs.csv"
        with open(file_path, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["category", "question", "keywords", "answer"])  # CSV Headers
            for faq in PolicyFAQ.objects.all():
                writer.writerow([faq.category, faq.question, faq.keywords, faq.answer])

        self.stdout.write(self.style.SUCCESS(f"Exported FAQs to {file_path}"))
