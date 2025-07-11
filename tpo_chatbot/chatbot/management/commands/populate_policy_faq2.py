import os
from django.core.management.base import BaseCommand
from chatbot.models import PolicyFAQ, PolicyFAQ2

class Command(BaseCommand):
    help = 'Populates the PolicyFAQ model with predefined data from PDFs.'

    def handle(self, *args, **kwargs):
        # Define the data structure for PolicyFAQ
        policy_data = [
            # Existing data entries...
            {
                "category": "Placement",
                "question": "What is the policy for students who receive a PPO (Pre-Placement Offer)?",
                "answer": "If a student receives a PPO, they can still participate in the placement process for one more offer from a company in the same or higher tier. However, they must inform the company not to consider them for PPO before it is released if they wish to be eligible for two offers.",
                "policy_type": "Placement",
                "academic_year": "2023-2024",
                "source": "230706_TPO-Policy-2.pdf",
                "applicable_to": "BTech",
            },
            {
                "category": "Placement",
                "question": "What is the policy for students who have one offer and receive a PPO afterward?",
                "answer": "If a student has one offer in hand and receives a PPO afterward, they can choose between the two offers. However, this will be considered a betterment switch, and they cannot apply for further betterment opportunities.",
                "policy_type": "Placement",
                "academic_year": "2023-2024",
                "source": "230706_TPO-Policy-2.pdf",
                "applicable_to": "BTech",
            },
            {
                "category": "Placement",
                "question": "What is the policy for students who are waitlisted by a company?",
                "answer": "If a student is waitlisted by a company and later receives an offer from another company, they can choose between the two offers. However, this will be counted as a betterment switch, and they cannot apply for further betterment opportunities.",
                "policy_type": "Placement",
                "academic_year": "2023-2024",
                "source": "230706_TPO-Policy-2.pdf",
                "applicable_to": "All",
            },
            {
                "category": "Internship",
                "question": "What is the policy for students who have secured an internship and wish to apply for placements?",
                "answer": "Students who have secured an internship are not eligible to apply for placements through the placement process.",
                "policy_type": "Internship",
                "academic_year": "2023-2024",
                "source": "230706_TPO-Policy-2.pdf",
                "applicable_to": "All",
            },
            {
                "category": "Internship",
                "question": "What is the policy for students who have secured a placement and wish to apply for internships?",
                "answer": "Students who have secured a placement are not eligible to apply for internships through the placement process.",
                "policy_type": "Internship",
                "academic_year": "2023-2024",
                "source": "230706_TPO-Policy-2.pdf",
                "applicable_to": "All",
            },
            {
                "category": "General",
                "question": "What is the policy for students who have secured both a placement and an internship?",
                "answer": "Students who have secured both a placement and an internship (I+P) are exempted from the placement process.",
                "policy_type": "General",
                "academic_year": "2023-2024",
                "source": "230706_TPO-Policy-2.pdf",
                "applicable_to": "All",
            },
            {
                "category": "General",
                "question": "What is the policy for students who have secured a placement and wish to apply for a better offer?",
                "answer": "Once a student has been placed in a company falling into a particular category, moving forward, they will be permitted to apply for only those companies which fall into a higher category than the one they are currently placed in. However, the betterment, i.e., getting placed in a company of a higher category, is restricted to only one time.",
                "policy_type": "General",
                "academic_year": "2023-2024",
                "source": "230706_TPO-Policy-2.pdf",
                "applicable_to": "All",
            },
            {
                "category": "General",
                "question": "What is the policy for students who have secured a placement and wish to pursue higher studies?",
                "answer": "If a student secures a placement but wishes to pursue higher studies, they need to inform the placement cell as soon as possible (latest by April end) along with the letter/offer received from the university.",
                "policy_type": "General",
                "academic_year": "2023-2024",
                "source": "placement-policy.pdf",
                "applicable_to": "All",
            },
            {
                "category": "General",
                "question": "What is the policy for students who have been blacklisted and wish to be removed from the blacklist?",
                "answer": "If a student is blacklisted, they can approach the placement committee to make a formal request for removal from the blacklist. If the committee rejects the request, the student can approach the director. The director's decision will be final and binding.",
                "policy_type": "General",
                "academic_year": "2023-2024",
                "source": "placement-policy.pdf",
                "applicable_to": "All",
            },
            {
                "category": "General",
                "question": "What is the policy for students who wish to participate in pool campus drives in other colleges?",
                "answer": "For pool campus drives in other colleges or if the company conducts any round outside the campus, the students who have registered/selected should compulsorily participate in the process. Students remaining absent in such cases will be debarred for any further placement opportunities.",
                "policy_type": "General",
                "academic_year": "2023-2024",
                "source": "placement-policy.pdf",
                "applicable_to": "All",
            },
        ]

        # Populate PolicyFAQ
        for item in policy_data:
            PolicyFAQ2.objects.update_or_create(
                category=item['category'],
                question=item['question'],
                defaults={
                    'answer': item['answer'],
                    'policy_type': item['policy_type'],
                    'academic_year': item['academic_year'],
                    'source': item['source'],
                    'applicable_to': item['applicable_to'],
                }
            )

        self.stdout.write(self.style.SUCCESS('Successfully populated the PolicyFAQ model with data.'))