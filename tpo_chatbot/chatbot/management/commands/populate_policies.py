from django.core.management.base import BaseCommand
from chatbot.models import PolicyFAQ

class Command(BaseCommand):
    help = 'Populates the PolicyFAQ model with predefined data.'

    def handle(self, *args, **kwargs):
        # List of predefined FAQs with categories, questions, answers, and keywords
        faqs =[
  {
    "category": "CTC Limit",
    "question": "What is the CTC limit for CE & IT students planning for higher studies?",
    "answer": "Students can apply only to companies offering ≤ 12 LPA.",
    "keywords": "CTC limit, CE, IT, higher studies, 12 LPA"
  },
  {
    "category": "CTC Limit",
    "question": "What is the maximum CTC for CE & IT students planning to pursue higher studies?",
    "answer": "Students can apply only to companies offering ≤ 12 LPA.",
    "keywords": "CTC limit, CE, IT, higher studies, 12 LPA"
  },
  {
    "category": "CTC Limit",
    "question": "What is the CTC cap for CE & IT students aiming for higher studies?",
    "answer": "Students can apply only to companies offering ≤ 12 LPA.",
    "keywords": "CTC limit, CE, IT, higher studies, 12 LPA"
  },
  {
    "category": "CTC Limit",
    "question": "What is the CTC threshold for CE & IT students planning to go for higher studies?",
    "answer": "Students can apply only to companies offering ≤ 12 LPA.",
    "keywords": "CTC limit, CE, IT, higher studies, 12 LPA"
  },
  {
    "category": "CTC Limit",
    "question": "What is the CTC restriction for CE & IT students considering higher studies?",
    "answer": "Students can apply only to companies offering ≤ 12 LPA.",
    "keywords": "CTC limit, CE, IT, higher studies, 12 LPA"
  },
  {
    "category": "Company Categorization",
    "question": "How are companies categorized for CE & IT branches?",
    "answer": "•	Normal: CTC < 18 LPA\n•	Dream: 18 LPA ≤ CTC < 40 LPA\n•	Super Dream: CTC ≥ 40 LPA",
    "keywords": "Company categorization, CE, IT, CTC, Normal, Dream, Super Dream"
  },
  {
    "category": "Company Categorization",
    "question": "What are the company categories for CE & IT branches?",
    "answer": "•	Normal: CTC < 18 LPA\n•	Dream: 18 LPA ≤ CTC < 40 LPA\n•	Super Dream: CTC ≥ 40 LPA",
    "keywords": "Company categorization, CE, IT, CTC, Normal, Dream, Super Dream"
  },
  {
    "category": "Company Categorization",
    "question": "How do companies get categorized for CE & IT branches?",
    "answer": "•	Normal: CTC < 18 LPA\n•	Dream: 18 LPA ≤ CTC < 40 LPA\n•	Super Dream: CTC ≥ 40 LPA",
    "keywords": "Company categorization, CE, IT, CTC, Normal, Dream, Super Dream"
  },
  {
    "category": "Company Categorization",
    "question": "What are the different company categories for CE & IT branches?",
    "answer": "•	Normal: CTC < 18 LPA\n•	Dream: 18 LPA ≤ CTC < 40 LPA\n•	Super Dream: CTC ≥ 40 LPA",
    "keywords": "Company categorization, CE, IT, CTC, Normal, Dream, Super Dream"
  },
  {
    "category": "Company Categorization",
    "question": "How are companies divided into categories for CE & IT branches?",
    "answer": "•	Normal: CTC < 18 LPA\n•	Dream: 18 LPA ≤ CTC < 40 LPA\n•	Super Dream: CTC ≥ 40 LPA",
    "keywords": "Company categorization, CE, IT, CTC, Normal, Dream, Super Dream"
  },
  {
    "category": "Betterment Rule",
    "question": "What is the betterment rule for CE & IT branches?",
    "answer": "•	Minimum betterment gap = 3 LPA.\n•	Only one betterment switch is permitted.",
    "keywords": "Betterment rule, CE, IT, betterment gap, 3 LPA, betterment switch"
  },
  {
    "category": "Betterment Rule",
    "question": "What are the betterment rules for CE & IT branches?",
    "answer": "•	Minimum betterment gap = 3 LPA.\n•	Only one betterment switch is permitted.",
    "keywords": "Betterment rule, CE, IT, betterment gap, 3 LPA, betterment switch"
  },
  {
    "category": "Betterment Rule",
    "question": "What is the minimum betterment gap for CE & IT branches?",
    "answer": "•	Minimum betterment gap = 3 LPA.\n•	Only one betterment switch is permitted.",
    "keywords": "Betterment rule, CE, IT, betterment gap, 3 LPA, betterment switch"
  },
  {
    "category": "Betterment Rule",
    "question": "What are the requirements for betterment in CE & IT branches?",
    "answer": "•	Minimum betterment gap = 3 LPA.\n•	Only one betterment switch is permitted.",
    "keywords": "Betterment rule, CE, IT, betterment gap, 3 LPA, betterment switch"
  },
  {
    "category": "Betterment Rule",
    "question": "What is the betterment policy for CE & IT branches?",
    "answer": "•	Minimum betterment gap = 3 LPA.\n•	Only one betterment switch is permitted.",
    "keywords": "Betterment rule, CE, IT, betterment gap, 3 LPA, betterment switch"
  },
  {
    "category": "Placement Commitment",
    "question": "After placement, is there a work commitment for CE & IT students?",
    "answer": "Yes, students must work for 1 year after joining.",
    "keywords": "Placement commitment, CE, IT, work commitment"
  },
  {
    "category": "Placement Commitment",
    "question": "Do CE & IT students have a work commitment after placement?",
    "answer": "Yes, students must work for 1 year after joining.",
    "keywords": "Placement commitment, CE, IT, work commitment"
  },
  {
    "category": "Placement Commitment",
    "question": "What is the work commitment for CE & IT students after placement?",
    "answer": "Yes, students must work for 1 year after joining.",
    "keywords": "Placement commitment, CE, IT, work commitment"
  },
  {
    "category": "Placement Commitment",
    "question": "Is there a mandatory work period for CE & IT students after placement?",
    "answer": "Yes, students must work for 1 year after joining.",
    "keywords": "Placement commitment, CE, IT, work commitment"
  },
  {
    "category": "Placement Commitment",
    "question": "What happens if CE & IT students do not fulfill their work commitment after placement?",
    "answer": "Yes, students must work for 1 year after joining.",
    "keywords": "Placement commitment, CE, IT, work commitment"
  },
  {
    "category": "Internship Policy",
    "question": "What is the policy for internships for CE & IT students?",
    "answer": "•	Only one internship offer allowed.\n•	Rejecting or not joining will lead to blacklisting.",
    "keywords": "Internship policy, CE, IT, internship offer, blacklisting"
  },
  {
    "category": "Internship Policy",
    "question": "What are the rules for internships for CE & IT students?",
    "answer": "•	Only one internship offer allowed.\n•	Rejecting or not joining will lead to blacklisting.",
    "keywords": "Internship policy, CE, IT, internship offer, blacklisting"
  },
  {
    "category": "Internship Policy",
    "question": "What is the internship policy for CE & IT students?",
    "answer": "•	Only one internship offer allowed.\n•	Rejecting or not joining will lead to blacklisting.",
    "keywords": "Internship policy, CE, IT, internship offer, blacklisting"
  },
  {
    "category": "Internship Policy",
    "question": "How are internships handled for CE & IT students?",
    "answer": "•	Only one internship offer allowed.\n•	Rejecting or not joining will lead to blacklisting.",
    "keywords": "Internship policy, CE, IT, internship offer, blacklisting"
  },
  {
    "category": "Internship Policy",
    "question": "What happens if a CE & IT student rejects their internship offer?",
    "answer": "•	Only one internship offer allowed.\n•	Rejecting or not joining will lead to blacklisting.",
    "keywords": "Internship policy, CE, IT, internship offer, blacklisting"
  }
]




        for faq in faqs:
            # Create or update each FAQ entry with keywords
            PolicyFAQ.objects.update_or_create(
                category=faq['category'],
                question=faq['question'],
                defaults={
                    'answer': faq['answer'],
                    'keywords': faq['keywords']
                }
            )

        self.stdout.write(self.style.SUCCESS('Successfully populated the PolicyFAQ model with data and keywords.'))