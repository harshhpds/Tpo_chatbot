import os
import re
import json
import PyPDF2
import cohere

from django.core.management.base import BaseCommand
from chatbot.models import PolicyFAQ  # Imported per instruction, though not used here.

class Command(BaseCommand):
    help = 'Generates training data from a policy PDF using Cohere-generated questions and saves it to a JSONL file.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--pdf',
            type=str,
            default="TPO VJTI POLICY 2024-25 (1).pdf",
            help="Path to the policy PDF file."
        )
        parser.add_argument(
            '--output',
            type=str,
            default="policy_training_data.jsonl",
            help="Output JSONL file for training data."
        )
        parser.add_argument(
            '--api_key',
            type=str,
            default='YOUR_COHERE_API_KEY',
            help="Cohere API key."
        )

    def extract_text_from_pdf(self, pdf_path):
        """Extracts text from the given PDF file."""
        text = ""
        with open(pdf_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text

    def generate_questions_for_paragraph(self, paragraph, cohere_client):
        """
        Uses Cohere's generation API to create questions based on the paragraph.
        Returns a list of questions.
        """
        prompt = (
            "Generate five relevant and concise questions based on the following text:\n\n"
            f"{paragraph}\n\n"
            "Questions:\n1."
        )
        try:
            response = cohere_client.generate(
                model="command-xlarge-nightly",  # Adjust model as needed
                prompt=prompt,
                max_tokens=200,
                temperature=0.7,
                stop_sequences=["\n\n"]
            )
            generated_text = response.generations[0].text.strip()
            # Split the output into individual questions using a regex pattern.
            questions = re.split(r'\n\d+\.', generated_text)
            questions = [q.strip() for q in questions if q.strip()]
            return questions
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error generating questions: {e}"))
            return []

    def create_training_examples(self, text, cohere_client):
        """
        Splits text into paragraphs and creates training examples.
        For each paragraph, uses Cohere to generate questions,
        then pairs each question with the paragraph as an answer.
        """
        paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
        training_examples = []
        for para in paragraphs:
            # Optionally ignore very short paragraphs
            if len(para) < 50:
                continue
            questions = self.generate_questions_for_paragraph(para, cohere_client)
            if not questions:
                questions = ["What does the policy state regarding the following section?"]
            for question in questions:
                example = {
                    "messages": [
                        {"role": "User", "content": question},
                        {"role": "Chatbot", "content": para}
                    ]
                }
                training_examples.append(example)
        return training_examples

    def save_to_jsonl(self, training_examples, output_file):
        """Saves the training examples to a JSONL file."""
        with open(output_file, "w", encoding="utf-8") as f:
            for example in training_examples:
                f.write(json.dumps(example) + "\n")

    def handle(self, *args, **options):
        pdf_path = options['pdf']
        output_file = options['output']
        api_key = options['api_key']

        cohere_client = cohere.Client(api_key)
        
        self.stdout.write(f"Extracting text from PDF: {pdf_path}")
        text = self.extract_text_from_pdf(pdf_path)
        self.stdout.write("Text extraction completed.")

        self.stdout.write("Generating training examples using Cohere...")
        training_examples = self.create_training_examples(text, cohere_client)
        
        if len(training_examples) < 100:
            self.stdout.write(self.style.WARNING(
                f"Warning: Only generated {len(training_examples)} examples. Consider revising the prompt or splitting the PDF content further."
            ))

        self.stdout.write(f"Saving {len(training_examples)} training examples to {output_file}")
        self.save_to_jsonl(training_examples, output_file)
        self.stdout.write(self.style.SUCCESS(f"Saved {len(training_examples)} training examples to {output_file}"))
