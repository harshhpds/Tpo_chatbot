import json
from django.core.management.base import BaseCommand
from chatbot.models import PolicyFAQ

class Command(BaseCommand):
    help = "Generate a JSONL file containing FAQs"

    def handle(self, *args, **kwargs):
        filename = "faq_data.jsonl"

        with open(filename, "w", encoding="utf-8") as file:
            faqs = PolicyFAQ.objects.all()
            for faq in faqs:
                conversation = {
                    "messages": [
                        {"role": "User", "content": faq.question},
                        {"role": "Chatbot", "content": faq.answer}
                    ]
                }
                file.write(json.dumps(conversation, ensure_ascii=False) + "\n")

        self.stdout.write(self.style.SUCCESS(f"Successfully created {filename}"))
