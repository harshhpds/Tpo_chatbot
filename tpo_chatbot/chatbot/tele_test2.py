import sys
import os
import re
import django
import logging
import random
import smtplib
from email.mime.text import MIMEText
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


from chatbot.models import FAQ, CompanyInfo, Internship, Student, PlacementRecord, QuickInfo
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

# Function to send OTP via email
def send_otp(email):
    otp = random.randint(100000, 999999)  # Generate a 6-digit OTP

    # Email configuration
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = "yuktakhairnar399@gmail.com"  
    sender_password = "hioemobjfdojbhsn"  
    # Email content
    subject = "Your OTP for TPO Chatbot Authentication"
    body = f"Your OTP is: {otp}. It is valid for 5 minutes."
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = email

    # Send email
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, email, msg.as_string())
        return otp
    except Exception as e:
        logger.error(f"Failed to send OTP: {e}")
        return None

# Telegram bot handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Welcome! Please enter your institute email address (e.g., xyz@mc.vjti.ac.in) for authentication.")
    context.user_data["state"] = "WAITING_FOR_EMAIL"

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Route logic based on the user's state
    state = context.user_data.get("state")

    if state == "WAITING_FOR_EMAIL":
        await handle_email(update, context)
    elif state == "WAITING_FOR_OTP":
        await handle_otp(update, context)
    elif state == "READY_TO_ASSIST":
        await handle_query(update, context)
    else:
        await update.message.reply_text("Please use the /start command to begin.")

async def handle_email(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    email = update.message.text

    # Validate email format and enforce the domain restriction
    if re.match(r"[^@\s]+@mc\.vjti\.ac\.in$", email):  # Check domain is @mc.vjti.ac.in
        otp = send_otp(email)
        if otp:
            context.user_data["email"] = email
            context.user_data["otp"] = otp
            context.user_data["state"] = "WAITING_FOR_OTP"
            await update.message.reply_text("An OTP has been sent to your email. Please enter the OTP to proceed.")
        else:
            await update.message.reply_text("Failed to send OTP. Please try again.")
    else:
        await update.message.reply_text("Invalid email address. Please use your institute email ending with @mc.vjti.ac.in.")

async def handle_otp(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_otp = update.message.text

    try:
        user_otp = int(user_otp)  # Convert input to integer
    except ValueError:
        await update.message.reply_text("Invalid OTP format. Please enter a numeric OTP.")
        return

    if context.user_data.get("otp") == user_otp:
        context.user_data["state"] = "READY_TO_ASSIST"
        await update.message.reply_text(
            "Authentication successful! Please choose an option to proceed:\n\n"
            "1. FAQs\n"
            "2. Placement Information\n"
            "3. Company Information\n"
            "4. Statistics\n"
            "5. Preparation Tips\n"
            "6. Internship Information\n"
            "7. Comparison\n"
            "Reply with the option number (e.g., '1' for FAQs)."
        )
    else:
        await update.message.reply_text("Invalid OTP. Please try again.")

async def handle_query(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text.lower()

    if user_message == "menu":
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
    if user_message == "1":
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

    faq_responses = {
        "1.1": "The TPO office is open from 9 AM to 5 PM on weekdays.",
        "1.2": "You can contact the TPO via email at tpo@example.com.",
        "1.3": "The head of the TPO department is Mr. John Doe.",
        "1.4": "The TPO office is located in Block B, Room 203."
    }

    if user_message in faq_responses:
        await update.message.reply_text(faq_responses[user_message])
        return

    # Placement Information
    if user_message == "2":
        response = (
            "Placement Information:\n"
            "1. Which company did a specific student get placed in?\n"
            "2. What package was offered to a specific student?\n"
            "Reply with the question number (e.g., '2.1' for company details)."
        )
        await update.message.reply_text(response)
        return

    if user_message == "2.1":
        await update.message.reply_text("Please enter the student's name to get placement details.")
        return

    if user_message == "2.2":
        await update.message.reply_text("Please enter the student's name to know the package offered.")
        return

    # Company Information
    if user_message == "3":
        response = (
            "Company Information:\n"
            "1. Tell me about a specific company.\n"
            "2. What is the selection process for a specific company?\n"
            "Reply with the question number (e.g., '3.1' for company details)."
        )
        await update.message.reply_text(response)
        return

    if user_message == "3.1":
        await update.message.reply_text("Please enter the company name to get details.")
        return

    if user_message == "3.2":
        await update.message.reply_text("Please enter the company name to know the selection process.")
        return

    # Internship Information
    if user_message == "6":
        response = (
            "Internship Information:\n"
            "1. Which internships are available?\n"
            "2. What is the eligibility criteria for internships?\n"
            "3. How can I apply for an internship?\n"
            "Reply with the question number (e.g., '6.1' for available internships)."
        )
        await update.message.reply_text(response)
        return

    if user_message == "6.1":
        internships = await sync_to_async(list)(Internship.objects.all())
        if internships:
            response = "Here are the available internships:\n"
            for internship in internships:
                response += (
                    f"- {internship.internship_title} at {internship.location}\n"
                    f"  Stipend: {internship.stipend} | Duration: {internship.duration}\n"
                    f"  Description: {internship.internship_description}\n"
                )
        else:
            response = "No internships are currently available."
        await update.message.reply_text(response)
        return

    if user_message == "6.2":
        response = (
            "Internship Eligibility Criteria:\n"
            "Please enter the internship title to get the eligibility details.\n"
            "Reply with 'eligibility: <Title>'(eg. eligibility:Frontend Intern )"
        )
        await update.message.reply_text(response)
        return

    if user_message.startswith("eligibility:"):
        internship_title = user_message.split(":", 1)[1].strip()
    
    # Use sync_to_async for querying and accessing the first object
        internship = await sync_to_async(lambda: Internship.objects.filter(internship_title__iexact=internship_title).first())()
    
        if internship:
            response = f"Eligibility for {internship_title}:\n{internship.eligibility}"
        else:
            response = f"No eligibility criteria found for {internship_title}."
    
        await update.message.reply_text(response)
        return

    if user_message == "6.3":
        response = (
            "How to Apply for Internships:\n"
            "Please enter the internship title to get the application link.\n"
            "Reply with 'apply: <Title>(eg. apply: Frontend Intern )"
        )
        await update.message.reply_text(response)
        return

    if user_message.startswith("apply:"):
        internship_title = user_message.split(":", 1)[1].strip()
        internship = await sync_to_async(lambda: Internship.objects.filter(internship_title__iexact=internship_title).first())()
        if internship:
            response = (
                f"You can apply for {internship_title} using the following link:\n"
                f"{internship.application_form_link}"
            )
        else:
            response = f"No application link found for {internship_title}."
        await update.message.reply_text(response)
        return

    await update.message.reply_text(
        "Invalid option! Please start again by typing 'Menu' and select a valid option."
    )
def main():
    application = Application.builder().token(settings.TELEGRAM_BOT_TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

    # Run the bot until manually stopped
    application.run_polling()

if __name__ == '__main__':
    main()