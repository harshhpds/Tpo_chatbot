import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tpo_chatbot.settings')
django.setup()

from chatbot.models import CompanyInfo, Role, Internship,PolicyFAQ

def populate_policy_faq():
    # Example FAQs based on the Placement Policy
    placement_policy_faqs = [
        {
            'question': "What is the eligibility for placement interviews?",
            'answer': "All registered and eligible students are allowed to appear for interviews until they secure a job.",
            'policy_category': "Placement Policy"
        },
        {
            'question': "How many offers can a student accept?",
            'answer': "A student can accept only one offer at the end of the day. For B.Tech students, only one offer is allowed, and for M.Tech and MCA students, only one job is permitted.",
            'policy_category': "Placement Policy"
        },
        {
            'question': "What happens if a student does not inform the Placement Cell about the decision on an offer?",
            'answer': "If a student fails to inform the Placement Cell about their decision, it will be assumed that the offer has been rejected.",
            'policy_category': "Placement Policy"
        },
        {
            'question': "What is the student code of conduct for placement interviews?",
            'answer': "Students must attend interviews in formal attire. Boys must be clean-shaven, and they must carry their identity card during the interview process.",
            'policy_category': "Placement Policy"
        },
        {
            'question': "Can a student quit the selection process once they start?",
            'answer': "Once a student begins the selection process for a company, they cannot quit mid-way. If they do, they will be debarred from future placement events.",
            'policy_category': "Placement Policy"
        }
    ]

    # Example FAQs based on the TPO VJTI Policy
    tpo_vjti_policy_faqs = [
        {
            'question': "When do companies release PPOs?",
            'answer': "Companies are requested to release their PPOs by the end of July, as the Final Placement process starts from August 1st.",
            'policy_category': "TPO VJTI Policy"
        },
        {
            'question': "What happens if a student receives a PPO after being placed in another company?",
            'answer': "If a student receives a PPO after already being placed in another company, they can select between the two offers. This counts as a betterment switch, and the student cannot apply for a better offer later.",
            'policy_category': "TPO VJTI Policy"
        },
        {
            'question': "What are the rules for internships in relation to placements?",
            'answer': "If a student has secured a placement, they can only apply for internships. If a student has secured both, they are exempt from the placement process.",
            'policy_category': "TPO VJTI Policy"
        },
        {
            'question': "What should a student do if they do not want to participate in placements?",
            'answer': "Students who do not want to participate in the placement process must submit a form declaring their intention not to participate.",
            'policy_category': "TPO VJTI Policy"
        },
        {
            'question': "Are students allowed to apply for the same company where they interned?",
            'answer': "Students who intern at a company are not permitted to apply for a placement with the same company.",
            'policy_category': "TPO VJTI Policy"
        }
    ]

    # Creating the FAQs in the database
    for faq_data in placement_policy_faqs + tpo_vjti_policy_faqs:
        PolicyFAQ.objects.create(
            question=faq_data['question'],
            answer=faq_data['answer'],
            policy_category=faq_data['policy_category']
        )

    print("Policy FAQs populated successfully!")

# Run the function to populate the FAQs
populate_policy_faq()
