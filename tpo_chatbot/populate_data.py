import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tpo_chatbot.settings')
django.setup()

from chatbot.models import CompanyInfo, Role, Internship

# Clear existing data (optional)
CompanyInfo.objects.all().delete()
Role.objects.all().delete()
Internship.objects.all().delete()

# Populate CompanyInfo
def populate_companies():
    companies = [
        {"company_name": "Tech Innovators", "description": "Leading tech solutions.", "contact_email": "info@techinnovators.com", "additional_info": "Global presence."},
        {"company_name": "Healthify Corp", "description": "Healthcare technology pioneer.", "contact_email": "contact@healthify.com", "additional_info": "Focus on AI-driven solutions."},
        {"company_name": "EduLearn", "description": "E-learning platform provider.", "contact_email": "support@edulearn.com", "additional_info": "Collaborates with universities."},
        {"company_name": "EcoWaves", "description": "Sustainable energy solutions.", "contact_email": "contact@ecowaves.com", "additional_info": "Renewable energy systems."},
        {"company_name": "FinTrack", "description": "Financial analytics and software.", "contact_email": "help@fintrack.com", "additional_info": "Specializes in blockchain."},
        {"company_name": "AgroTech", "description": "Agricultural innovations.", "contact_email": "info@agrotech.com", "additional_info": "Smart farming solutions."},
        {"company_name": "AutoDrive", "description": "Autonomous vehicle manufacturer.", "contact_email": "careers@autodrive.com", "additional_info": "Focus on AI and ML."},
        {"company_name": "BuildWell", "description": "Construction technology.", "contact_email": "info@buildwell.com", "additional_info": "3D printing for buildings."},
        {"company_name": "ShopEase", "description": "E-commerce giant.", "contact_email": "support@shopease.com", "additional_info": "Operates globally."},
        {"company_name": "MediCare Plus", "description": "Healthcare provider.", "contact_email": "info@medicareplus.com", "additional_info": "Focus on patient care."},
    ]

    for company in companies:
        CompanyInfo.objects.create(**company)

# Populate Role
def populate_roles():
    companies = list(CompanyInfo.objects.all())
    roles = [
        {"company": companies[0], "role_title": "Software Developer", "role_description": "Develops software applications.", "salary_package": 6.5, "location": "Bangalore", "eligibility": "B.Tech/M.Tech in CS/IT", "application_form_link": "https://apply.techinnovators.com", "hr_number": "1234567890"},
        {"company": companies[1], "role_title": "Data Analyst", "role_description": "Analyzes healthcare data.", "salary_package": 5.5, "location": "Pune", "eligibility": "B.Sc/M.Sc in Data Science", "application_form_link": "https://apply.healthify.com", "hr_number": "9876543210"},
        # Add 8 more roles with unique details
    ]

    for role in roles:
        Role.objects.create(**role)

# Populate Internship
def populate_internships():
    companies = list(CompanyInfo.objects.all())
    internships = [
        {"company": companies[0], "internship_title": "Frontend Intern", "internship_description": "UI/UX development.", "stipend": 15000, "duration": "2 months", "location": "Remote", "eligibility": "Undergraduate in CS", "application_form_link": "https://intern.techinnovators.com", "mentor_contact": "1234567890"},
        {"company": companies[1], "internship_title": "Research Intern", "internship_description": "Healthcare data research.", "stipend": 12000, "duration": "3 months", "location": "Delhi", "eligibility": "Masters in Bioinformatics", "application_form_link": "https://intern.healthify.com", "mentor_contact": "9876543210"},
        # Add 8 more internships with unique details
    ]

    for internship in internships:
        Internship.objects.create(**internship)

if __name__ == "__main__":
    populate_companies()
    populate_roles()
    populate_internships()
    print("Data populated successfully!")
