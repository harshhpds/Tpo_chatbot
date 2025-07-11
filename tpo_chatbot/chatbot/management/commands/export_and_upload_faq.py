import cohere
from django.core.management.base import BaseCommand
from chatbot.models import PolicyFAQ

class Command(BaseCommand):
    help = 'Uses Cohere pre-trained model to generate responses for FAQs.'

    def handle(self, *args, **kwargs):
        COHERE_API_KEY = "8CsCDBsCyyDQriHfwCj0AAz3sGRF66szhdxt75fw"  # Replace with your actual API key

        co = cohere.Client(api_key=COHERE_API_KEY)

        # Fetch FAQs from your database
        faqs = PolicyFAQ.objects.all()

        # Example: Generate responses for each FAQ
        for faq in faqs:
            prompt = f"Q: {faq.question}\nA:"
            response = co.generate(
                model="command-r",  # Use a pre-trained model
                prompt=prompt,
                max_tokens=100
            )

            # Print or save the generated response
            self.stdout.write(self.style.SUCCESS(f"Q: {faq.question}"))
            self.stdout.write(self.style.SUCCESS(f"A: {response.generations[0].text}"))