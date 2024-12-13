import os
import django
from datetime import date, timedelta
from decimal import Decimal
import random

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tpo_chatbot.settings')  # Adjust as per your settings module
django.setup()

from chatbot.models import FAQ, CompanyInfo, Student, PlacementRecord, QuickInfo

def populate_faq():
    questions_answers = [
        ("What are the office hours?", "The office is open from 9 AM to 5 PM on weekdays."),
        ("How can I contact the TPO?", "You can contact the TPO via email at tpo@example.com."),
        ("Who is the head of the TPO?", "The head of the TPO department is Mr. John Doe."),
        ("Where is the TPO office located?", "The TPO office is in Block B, Room 203."),
        ("What documents are required for placement?", "You need your resume, ID proof, and academic transcripts."),
        ("What companies are visiting this year?", "A variety of companies from tech, finance, and consultancy sectors."),
        ("What is the average package?", "The average package this year is 6 LPA."),
        ("How can I apply for internships?", "You can apply through the TPO portal."),
        ("What are the eligibility criteria?", "Eligibility depends on the specific company’s requirements."),
        ("When will the placement season start?", "The placement season starts in August."),
    ]
    
    for question, answer in questions_answers:
        FAQ.objects.get_or_create(question=question, answer=answer)

def populate_company_info():
    companies = [
        ("TechCorp", "Leading tech company specializing in AI solutions.", "hr@techcorp.com", "Located in Silicon Valley."),
        ("DataWorks", "Data analysis and solutions provider.", "recruitment@dataworks.com", "Specializes in big data."),
        ("FinServe", "Financial services company.", "jobs@finserve.com", "Known for great work culture."),
        ("MediCare", "Healthcare tech company.", "contact@medicare.com", "Focuses on telemedicine."),
        ("EduFuture", "E-learning platform.", "careers@edufuture.com", "Provides online education solutions."),
        ("BuildIt", "Construction and real estate firm.", "hr@buildit.com", "Specializes in sustainable buildings."),
        ("EcoGreen", "Environmental and renewable energy company.", "careers@ecogreen.com", "Focuses on eco-friendly solutions."),
        ("RetailZone", "Retail solutions provider.", "hr@retailzone.com", "Leader in retail technology."),
        ("AgriCorp", "Agricultural tech company.", "jobs@agricorp.com", "Provides modern solutions for agriculture."),
        ("SafeBank", "Banking and finance institution.", "recruitment@safebank.com", "Known for high compensation packages."),
    ]
    
    for name, description, email, info in companies:
        CompanyInfo.objects.get_or_create(
            company_name=name,
            description=description,
            contact_email=email,
            additional_info=info
        )

def populate_students():
    branches = ["CSE", "ECE", "ME", "CE", "EE"]
    for i in range(10):
        student_id = f"S{i+1:03}"
        name = f"Student {i+1}"
        branch = random.choice(branches)
        year_of_study = random.randint(1, 4)
        
        Student.objects.get_or_create(
            student_id=student_id,
            name=name,
            branch=branch,
            year_of_study=year_of_study
        )

def populate_placement_records():
    students = Student.objects.all()
    companies = CompanyInfo.objects.all()
    
    for student in students:
        company = random.choice(companies)
        package = Decimal(random.uniform(3, 15)).quantize(Decimal("0.00"))
        placement_date = date.today() - timedelta(days=random.randint(0, 365))
        
        PlacementRecord.objects.get_or_create(
            student=student,
            company=company,
            package=package,
            placement_date=placement_date
        )

def populate_quick_info():
    quick_info_data = [
        ("office_hours", "The TPO office is open from 9 AM to 5 PM on weekdays."),
        ("contact_info", "You can reach us at tpo@example.com or call 123-456-7890."),
        ("head_of_tpo", "Mr. John Doe"),
        ("tpo_location", "Block B, Room 203"),
        ("placement_start_date", "The placement season begins in August."),
        ("average_package", "The average package is 6 LPA."),
        ("highest_package", "The highest package this year is 15 LPA."),
        ("internship_info", "Internships are available for students in their final year."),
        ("cgpa_requirement", "A minimum CGPA of 7.0 is required."),
        ("upcoming_events", "Upcoming placement drive on September 15th."),
    ]
    
    for key, value in quick_info_data:
        QuickInfo.objects.get_or_create(info_key=key, info_value=value)

def run():
    print("Populating FAQ table...")
    populate_faq()
    print("Populating CompanyInfo table...")
    populate_company_info()
    print("Populating Student table...")
    populate_students()
    print("Populating PlacementRecord table...")
    populate_placement_records()
    print("Populating QuickInfo table...")
    populate_quick_info()
    print("Data population complete.")

if __name__ == "__main__":
    run()
