import google.generativeai as genai
from django.core.management.base import BaseCommand
from chatbot.models import PolicyFAQ, PolicyFAQ2

class Command(BaseCommand):
    help = "Generate and store embeddings for PolicyFAQ and PolicyFAQ2 using the text-embedding-004 model."

    def handle(self, *args, **kwargs):
        # Configure the Gemini API with your API key.
        genai.configure(api_key="AIzaSyCpjHqW6t4oSg1Ge_zYcag854fqGVYwdXA")  # Replace with your actual key

        def generate_embedding(text):
            """
            Generate an embedding for the given text using embed_content with the text-embedding-004 model.
            """
            try:
                response = genai.embed_content("models/text-embedding-004", content=text)
                return response.get("embedding")
            except Exception as e:
                print("Error generating embedding:", e)
                return None

        self.stdout.write("Processing PolicyFAQ model...")
        for faq in PolicyFAQ.objects.all():
            if not faq.embedding:  # Only generate if embedding is not already set.
                embedding = generate_embedding(faq.question)
                if embedding:
                    faq.embedding = embedding
                    faq.save()
                else:
                    self.stdout.write(f"Skipping FAQ (ID: {faq.id}) due to embedding error.")
        self.stdout.write(self.style.SUCCESS("✅ PolicyFAQ embeddings generated and saved."))


        self.stdout.write(self.style.SUCCESS("🎉 Embedding generation completed successfully!"))
