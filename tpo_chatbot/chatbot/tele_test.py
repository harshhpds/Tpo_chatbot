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
    user_message = update.message.text.lower()

    # Provide options for the user to select
    if user_message == "/start":
        response = (
            "Welcome! Please choose an option to proceed:\n\n"
            "1. FAQs\n"
            "2. Placement Information\n"
            "3. Company Information\n"
            "4. Statistics\n"
            "5. Preparation Tips\n"
            "6. Internship Information\n"
            "7. Comparison\n"
            "Reply with the option number (e.g., '1' for FAQs)."
        )
        await update.message.reply_text(response)
        return

    # FAQs
    elif user_message == "1":
        response = (
            "FAQs:\n"
            "1. What are the TPO office hours?\n"
            "2. How can I contact the TPO?\n"
            "3. Who is the head of the TPO department?\n"
            "4. Where is the TPO office located?\n"
            "Reply with the question number (e.g., '1' for TPO office hours)."
        )
        await update.message.reply_text(response)
        return

    elif user_message == "1.1":
        await update.message.reply_text("The TPO office is open from 9 AM to 5 PM on weekdays.")
    elif user_message == "1.2":
        await update.message.reply_text("You can contact the TPO via email at tpo@example.com.")
    elif user_message == "1.3":
        await update.message.reply_text("The head of the TPO department is Mr. John Doe.")
    elif user_message == "1.4":
        await update.message.reply_text("The TPO office is located in Block B, Room 203.")

    # Placement Information
    elif user_message == "2":
        response = (
            "Placement Information:\n"
            "1. Which company did a specific student get placed in?\n"
            "2. What package was offered to a specific student?\n"
            "Reply with the question number (e.g., '2.1' for company details)."
        )
        await update.message.reply_text(response)
        return

    elif user_message == "2.1":
        await update.message.reply_text("Please enter the student's name to get placement details.")
    elif user_message == "2.2":
        await update.message.reply_text("Please enter the student's name to know the package offered.")

    # Company Information
    elif user_message == "3":
        response = (
            "Company Information:\n"
            "1. Tell me about a specific company.\n"
            "2. What is the selection process for a specific company?\n"
            "Reply with the question number (e.g., '3.1' for company details)."
        )
        await update.message.reply_text(response)
        return

    elif user_message == "3.1":
        await update.message.reply_text("Please enter the company name to get details.")
    elif user_message == "3.2":
        await update.message.reply_text("Please enter the company name to know the selection process.")

    # Additional sections like 'Statistics', 'Preparation Tips', etc., can be formatted similarly.

    else:
        await update.message.reply_text(
            "Invalid option! Please start again by typing '/start' and select a valid option."
        )



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Display the initial welcome message and the options menu
    response = (
        "Hello! I am your TPO chatbot. How can I assist you today?\n\n"
        "Welcome! Please choose an option to proceed:\n\n"
        "1. FAQs\n"
        "2. Placement Information\n"
        "3. Company Information\n"
        "4. Statistics\n"
        "5. Preparation Tips\n"
        "6. Internship Information\n"
        "7. Comparison\n"
        "Reply with the option number (e.g., '1' for FAQs)."
    )
    await update.message.reply_text(response)

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
