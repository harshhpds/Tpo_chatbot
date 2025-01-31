from django.core.management.base import BaseCommand
from chatbot.models import PolicyFAQ


class Command(BaseCommand):
    help = 'Populates the PolicyFAQ model with predefined data.'

    def handle(self, *args, **kwargs):
        # List of predefined FAQs with categories, questions, answers, and keywords
        faqs = [
            # Missing entries with variations
            {"category": "TPO Policy", "question": "Is there any restriction on the number of placement opportunities for BTech students?", "answer": "Yes, a BTech student can apply for only two offers, including the PPO.", "keywords": "BTech, placement opportunities, restriction"},
            {"category": "TPO Policy", "question": "Can BTech students apply for more than two placement offers?", "answer": "Yes, a BTech student can apply for only two offers, including the PPO.", "keywords": "BTech, placement opportunities, restriction"},
            {"category": "TPO Policy", "question": "How many placement offers can a BTech student apply for?", "answer": "Yes, a BTech student can apply for only two offers, including the PPO.", "keywords": "BTech, placement opportunities, restriction"},
            {"category": "TPO Policy", "question": "What is the limit on placement offers for BTech students?", "answer": "Yes, a BTech student can apply for only two offers, including the PPO.", "keywords": "BTech, placement opportunities, restriction"},
            {"category": "TPO Policy", "question": "Can BTech students get more than two placement offers?", "answer": "Yes, a BTech student can apply for only two offers, including the PPO.", "keywords": "BTech, placement opportunities, restriction"},

            {"category": "TPO Policy", "question": "What happens if a student gets offers from two companies simultaneously?", "answer": "The student can choose between the two companies, but this will count as their betterment switch.", "keywords": "simultaneous offers, betterment switch"},
            {"category": "TPO Policy", "question": "Can a student accept two offers at the same time?", "answer": "The student can choose between the two companies, but this will count as their betterment switch.", "keywords": "simultaneous offers, betterment switch"},
            {"category": "TPO Policy", "question": "What if a student receives two offers simultaneously?", "answer": "The student can choose between the two companies, but this will count as their betterment switch.", "keywords": "simultaneous offers, betterment switch"},
            {"category": "TPO Policy", "question": "How does a student handle receiving two offers at once?", "answer": "The student can choose between the two companies, but this will count as their betterment switch.", "keywords": "simultaneous offers, betterment switch"},
            {"category": "TPO Policy", "question": "What if a student gets multiple offers at the same time?", "answer": "The student can choose between the two companies, but this will count as their betterment switch.", "keywords": "simultaneous offers, betterment switch"},

            {"category": "TPO Policy", "question": "Are internships offered during academic overlap allowed?", "answer": "No, internships that overlap with academic activities are not allowed as per the institute’s academic calendar.", "keywords": "internships, academic overlap"},
            {"category": "TPO Policy", "question": "Can students do internships that overlap with academic activities?", "answer": "No, internships that overlap with academic activities are not allowed as per the institute’s academic calendar.", "keywords": "internships, academic overlap"},
            {"category": "TPO Policy", "question": "Is it allowed to have internships during academic terms?", "answer": "No, internships that overlap with academic activities are not allowed as per the institute’s academic calendar.", "keywords": "internships, academic overlap"},
            {"category": "TPO Policy", "question": "Can students participate in internships that overlap with academic sessions?", "answer": "No, internships that overlap with academic activities are not allowed as per the institute’s academic calendar.", "keywords": "internships, academic overlap"},
            {"category": "TPO Policy", "question": "Are internships during academic terms permitted?", "answer": "No, internships that overlap with academic activities are not allowed as per the institute’s academic calendar.", "keywords": "internships, academic overlap"},

            {"category": "TPO Policy", "question": "What is the TPO's role in resolving academic issues during placements?", "answer": "The TPO has no say in academic and examination-related matters.", "keywords": "TPO, academic issues, placement"},
            {"category": "TPO Policy", "question": "Does the TPO handle academic issues during placements?", "answer": "The TPO has no say in academic and examination-related matters.", "keywords": "TPO, academic issues, placement"},
            {"category": "TPO Policy", "question": "What role does the TPO play in academic matters during placements?", "answer": "The TPO has no say in academic and examination-related matters.", "keywords": "TPO, academic issues, placement"},
            {"category": "TPO Policy", "question": "Is the TPO involved in academic issues during placements?", "answer": "The TPO has no say in academic and examination-related matters.", "keywords": "TPO, academic issues, placement"},
            {"category": "TPO Policy", "question": "How does the TPO handle academic issues during placements?", "answer": "The TPO has no say in academic and examination-related matters.", "keywords": "TPO, academic issues, placement"},

            {"category": "TPO Policy", "question": "Can a student apply for companies below their current placement category?", "answer": "No, students can only apply for companies in a higher category than their current placement.", "keywords": "placement category, apply, companies"},
            {"category": "TPO Policy", "question": "Are students allowed to apply for companies in a lower category?", "answer": "No, students can only apply for companies in a higher category than their current placement.", "keywords": "placement category, apply, companies"},
            {"category": "TPO Policy", "question": "Can students apply for companies in a lower placement category?", "answer": "No, students can only apply for companies in a higher category than their current placement.", "keywords": "placement category, apply, companies"},
            {"category": "TPO Policy", "question": "Is it allowed to apply for companies in a lower placement category?", "answer": "No, students can only apply for companies in a higher category than their current placement.", "keywords": "placement category, apply, companies"},
            {"category": "TPO Policy", "question": "Can students apply for companies in a lower tier than their current placement?", "answer": "No, students can only apply for companies in a higher category than their current placement.", "keywords": "placement category, apply, companies"},

            {"category": "TPO Policy", "question": "What does the 'One student, One internship' policy mean?", "answer": "This policy means that each student can secure only one internship offer.", "keywords": "One student, One internship, policy"},
            {"category": "TPO Policy", "question": "Can a student get more than one internship offer?", "answer": "This policy means that each student can secure only one internship offer.", "keywords": "One student, One internship, policy"},
            {"category": "TPO Policy", "question": "Is it possible to get multiple internship offers?", "answer": "This policy means that each student can secure only one internship offer.", "keywords": "One student, One internship, policy"},
            {"category": "TPO Policy", "question": "Can students have more than one internship offer?", "answer": "This policy means that each student can secure only one internship offer.", "keywords": "One student, One internship, policy"},
            {"category": "TPO Policy", "question": "Are students allowed to get multiple internship offers?", "answer": "This policy means that each student can secure only one internship offer.", "keywords": "One student, One internship, policy"},

            {"category": "TPO Policy", "question": "How is the final decision regarding discrepancies in placements made?", "answer": "The final decision is made by the Professor-in-Charge, Training and Placement Office, VJTI.", "keywords": "discrepancies, final decision, placements"},
            {"category": "TPO Policy", "question": "Who makes the final decision on placement discrepancies?", "answer": "The final decision is made by the Professor-in-Charge, Training and Placement Office, VJTI.", "keywords": "discrepancies, final decision, placements"},
            {"category": "TPO Policy", "question": "How are placement discrepancies resolved?", "answer": "The final decision is made by the Professor-in-Charge, Training and Placement Office, VJTI.", "keywords": "discrepancies, final decision, placements"},
            {"category": "TPO Policy", "question": "Who resolves placement discrepancies?", "answer": "The final decision is made by the Professor-in-Charge, Training and Placement Office, VJTI.", "keywords": "discrepancies, final decision, placements"},
            {"category": "TPO Policy", "question": "What is the process for resolving placement discrepancies?", "answer": "The final decision is made by the Professor-in-Charge, Training and Placement Office, VJTI.", "keywords": "discrepancies, final decision, placements"},

            {"category": "TPO Policy", "question": "Are internships mandatory for MCA students to be eligible for placements?", "answer": "Yes, MCA students who qualify for an internship are eligible for placements.", "keywords": "MCA, internships, placements"},
            {"category": "TPO Policy", "question": "Do MCA students need to do an internship to be eligible for placements?", "answer": "Yes, MCA students who qualify for an internship are eligible for placements.", "keywords": "MCA, internships, placements"},
            {"category": "TPO Policy", "question": "Is an internship required for MCA students to be eligible for placements?", "answer": "Yes, MCA students who qualify for an internship are eligible for placements.", "keywords": "MCA, internships, placements"},
            {"category": "TPO Policy", "question": "Can MCA students be placed without an internship?", "answer": "Yes, MCA students who qualify for an internship are eligible for placements.", "keywords": "MCA, internships, placements"},
            {"category": "TPO Policy", "question": "Are MCA students required to do an internship to be eligible for placements?", "answer": "Yes, MCA students who qualify for an internship are eligible for placements.", "keywords": "MCA, internships, placements"},

            {"category": "TPO Policy", "question": "Can students switch companies after getting an offer from the waitlist?", "answer": "Yes, but this will count as their one-time betterment switch.", "keywords": "waitlist, switch companies, betterment switch"},
            {"category": "TPO Policy", "question": "Is it possible to switch companies after getting an offer from the waitlist?", "answer": "Yes, but this will count as their one-time betterment switch.", "keywords": "waitlist, switch companies, betterment switch"},
            {"category": "TPO Policy", "question": "Can students change companies after getting an offer from the waitlist?", "answer": "Yes, but this will count as their one-time betterment switch.", "keywords": "waitlist, switch companies, betterment switch"},
            {"category": "TPO Policy", "question": "Is it allowed to switch companies after getting an offer from the waitlist?", "answer": "Yes, but this will count as their one-time betterment switch.", "keywords": "waitlist, switch companies, betterment switch"},
            {"category": "TPO Policy", "question": "Can students switch to another company after getting an offer from the waitlist?", "answer": "Yes, but this will count as their one-time betterment switch.", "keywords": "waitlist, switch companies, betterment switch"},
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