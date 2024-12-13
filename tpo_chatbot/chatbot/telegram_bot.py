import sys
import os
# Add the root directory of your Django project to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import sys
import os
import re
import django
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from asgiref.sync import sync_to_async

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Set up Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tpo_chatbot.settings")
django.setup()

from chatbot.models import FAQ, CompanyInfo, Student, PlacementRecord, QuickInfo
from django.conf import settings

def preprocess_query(query: str):
    tokens = re.findall(r'\b\w+\b', query.lower())
    return tokens

def identify_intent(tokens):
    intents = {
        'faqs': ['hours', 'contact', 'head', 'location', 'what does'],
        'placement_info': ['company', 'placed', 'package', 'branch', 'students'],
        'company_info': ['tell me about', 'selection process', 'roles', 'average package'],
        'statistics': ['how many', 'average', 'median', 'trend'],
        'preparation': ['eligibility', 'prepare', 'workshops', 'cgpa'],
        'internship_info': ['internship', 'apply', 'companies'],
        'comparison': ['highest package', 'compare', 'top companies'],
    }
    
    for intent, keywords in intents.items():
        if any(keyword in tokens for keyword in keywords):
            return intent
    return 'miscellaneous'

async def handle_query(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text
    tokens = preprocess_query(user_message)
    intent = identify_intent(tokens)

    response = "I'm sorry, I didn't understand your question."
    # Intent handling based on identified intents from keywords
    if intent == 'faqs':
        if "hours" in tokens:
                response = "The TPO office is open from 9 AM to 5 PM on weekdays."
        elif "contact" in tokens:
            response = "You can contact the TPO via email at tpo@example.com."
        elif "head" in tokens:
            response = "The head of the TPO department is Mr. John Doe."
        elif "location" in tokens:
            response = "The TPO office is located in Block B, Room 203."
        elif "what does" in tokens:
            response = "The TPO department assists with placements, internships, and career guidance."

    elif intent == 'placement_info':
        if "company" in tokens and "placed" in tokens:
            student_name = user_message.split("which company did")[-1].split("get placed")[0].strip()
            try:
                student = await sync_to_async(Student.objects.get)(name__iexact=student_name)
                placement = await sync_to_async(PlacementRecord.objects.get)(student=student)
                response = f"{student.name} got placed in {placement.company.company_name}."
            except (Student.DoesNotExist, PlacementRecord.DoesNotExist):
                response = "I'm sorry, I couldn't find any placement information for that student."

        elif "package" in tokens and "offered to" in user_message:
            student_name = user_message.split("package offered to")[-1].strip()
            try:
                student = await sync_to_async(Student.objects.get)(name__iexact=student_name)
                placement = await sync_to_async(PlacementRecord.objects.get)(student=student)
                response = f"The package offered to {student.name} was {placement.package} LPA."
            except (Student.DoesNotExist, PlacementRecord.DoesNotExist):
                response = "I couldn't find any package information for that student."

    elif intent == 'company_info':
        if "tell me about" in tokens:
            company_name = user_message.split("tell me about")[-1].strip()
            try:
                company_info = await sync_to_async(CompanyInfo.objects.get)(company_name__iexact=company_name)
                response = f"{company_info.company_name} details: {company_info.description}."
            except CompanyInfo.DoesNotExist:
                response = "I'm sorry, I couldn't find any information about that company."
        elif "selection process" in tokens:
            company_name = user_message.split("selection process for")[-1].strip()
            response = f"I currently don't have specific selection process information for {company_name}."

    elif intent == 'statistics':
        if "how many" in tokens and "students placed this year" in user_message:
            # Implement query to get the count of students placed this year
            response = f"A total of X students were placed this year."
        elif "average" in tokens and "branch" in user_message:
            branch_name = user_message.split("average package for students in")[-1].strip()
        # Implement query to fetch the average package for the branch
            response = f"The average package for {branch_name} students is X LPA."

    elif intent == 'preparation':
        if "eligibility" in tokens:
            response = "Eligibility criteria vary by company, but generally, a minimum CGPA of 7.0 is required."
        elif "prepare" in tokens:
            company_name = user_message.split("prepare for placements in")[-1].strip()
            response = f"To prepare for placements in {company_name}, focus on relevant technical and soft skills."

    elif intent == 'internship_info':
        if "internship" in tokens:
            response = "The TPO department offers various internship opportunities for eligible students."
        elif "apply" in tokens and "internships" in user_message:
            response = "You can apply for internships through the TPO portal."

    elif intent == 'comparison':
        if "highest package" in tokens:
            # Implement query to get the company offering the highest package this year
            response = "The highest package this year was offered by Company XYZ at 15 LPA."
        elif "compare" in tokens and "packages" in user_message:
            company_name = user_message.split("compare packages for")[-1].strip()
        # Implement query to compare packages for the specified company
            response = f"Here’s how {company_name}'s packages compare with others."

    else:  # Miscellaneous
        response = "I'm sorry, I don't have information on that topic."

    await update.message.reply_text(response)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Hello! I am your TPO chatbot. How can I assist you today?")

def main():
    application = Application.builder().token(settings.TELEGRAM_BOT_TOKEN).build()
    
    # Add the /start command handler
    application.add_handler(CommandHandler("start", start))
    
    # Add the asynchronous message handler
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_query))

    # Run the bot until manually stopped
    application.run_polling()

if __name__ == '__main__':
    main()
