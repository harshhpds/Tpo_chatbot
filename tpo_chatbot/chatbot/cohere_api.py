import sys
import os
import re
import django
import logging
import random
import smtplib
from email.mime.text import MIMEText
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from asgiref.sync import sync_to_async
from django.conf import settings
import cohere
from django.db.models import Q  # Correct import for Q object

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Set up Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tpo_chatbot.settings")
django.setup()

from chatbot.models import FAQ, CompanyInfo, Internship, PlacementStatistics, PolicyFAQ, Role, Student, PlacementRecord

# Initialize Cohere client
cohere_client = cohere.Client(api_key='8CsCDBsCyyDQriHfwCj0AAz3sGRF66szhdxt75fw')

# Function to send OTP via email
def send_otp(email):
    otp = random.randint(100000, 999999)
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = "harsh.hpds@gmail.com"
    sender_password = "fqhcumomzvqtvgoy"

    subject = "Your OTP for TPO Chatbot Authentication"
    body = f"Your OTP is: {otp}. It is valid for 5 minutes."
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = email

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, email, msg.as_string())
        return otp
    except Exception as e:
        logger.error(f"Failed to send OTP: {e}")
        return None

# /start command handler: Sends the main menu inline keyboard.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Welcome! Please enter your institute email address (e.g., xyz@mc.vjti.ac.in) for authentication.")
    context.user_data["state"] = "WAITING_FOR_EMAIL"

# CallbackQuery handler: Processes button clicks.
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    selected_option = query.data

    if selected_option == "faqs":
        keyboard = [
            [InlineKeyboardButton("What are the TPO office hours?", callback_data="faq_1")],
            [InlineKeyboardButton("How can I contact the TPO?", callback_data="faq_2")],
            [InlineKeyboardButton("Who is the head of the TPO department?", callback_data="faq_3")],
            [InlineKeyboardButton("Where is the TPO office located?", callback_data="faq_4")],
            [InlineKeyboardButton("Back", callback_data="back")]
        ]
        response_text = "Please choose an option under FAQs:"
    elif selected_option == "placement":
        keyboard = [
            [InlineKeyboardButton("Company Placement Records", callback_data="placement_1")],
            [InlineKeyboardButton("Branch-wise Placement Statistics", callback_data="placement_2")],
            [InlineKeyboardButton("Year-wise Placement Trends", callback_data="placement_3")],
            [InlineKeyboardButton("Back", callback_data="back")]
        ]
        response_text = "Please choose an option under Placement Information:"
    elif selected_option == "company":
        keyboard = [
            [InlineKeyboardButton("Tell me about a specific company", callback_data="company_1")],
            [InlineKeyboardButton("What is the selection process for a specific company?", callback_data="company_2")],
            [InlineKeyboardButton("Back", callback_data="back")]
        ]
        response_text = "Please choose an option under Company Information:"
    elif selected_option == "statistics":
        keyboard = [
            [InlineKeyboardButton("Placement Rate", callback_data="statistics_1")],
            [InlineKeyboardButton("Salary Statistics", callback_data="statistics_2")],
            [InlineKeyboardButton("Top Recruiting Companies", callback_data="statistics_3")],
            [InlineKeyboardButton("Back", callback_data="back")]
        ]
        response_text = "Please choose an option under Statistics:"
    elif selected_option == "preparation":
        keyboard = [
            [InlineKeyboardButton("Aptitude Test Preparation", callback_data="preparation_1")],
            [InlineKeyboardButton("Technical Interview Preparation", callback_data="preparation_2")],
            [InlineKeyboardButton("HR Interview Preparation", callback_data="preparation_3")],
            [InlineKeyboardButton("Group Discussion Tips", callback_data="preparation_4")],
            [InlineKeyboardButton("Resume Building", callback_data="preparation_5")],
            [InlineKeyboardButton("Back", callback_data="back")]
        ]
        response_text = "Please choose an option under Preparation Tips:"
    elif selected_option == "internship":
        keyboard = [
            [InlineKeyboardButton("Available Internships", callback_data="internship_1")],
            [InlineKeyboardButton("Eligibility Criteria", callback_data="internship_2")],
            [InlineKeyboardButton("How to Apply", callback_data="internship_3")],
            [InlineKeyboardButton("Back", callback_data="back")]
        ]
        response_text = "Please choose an option under Internship Information:"
    elif selected_option == "policies":
        keyboard = [
            [InlineKeyboardButton("Deadline for PPOs", callback_data="policy_1")],
            [InlineKeyboardButton("Accepting Multiple Offers", callback_data="policy_2")],
            [InlineKeyboardButton("Opting Out of Placement", callback_data="policy_3")],
            [InlineKeyboardButton("Declining Job Offers", callback_data="policy_4")],
            [InlineKeyboardButton("Minimum CTC for Unplaced Students", callback_data="policy_5")],
            [InlineKeyboardButton("Other Policy Questions", callback_data="policy_6")],
            [InlineKeyboardButton("Back", callback_data="back")]
        ]
        response_text = "Please choose an option under Policies:"
    elif selected_option == "policy_6":
        # Trigger Cohere for "Other Policy Questions"
        context.user_data["state"] = "WAITING_FOR_POLICY_QUESTION"
        response_text = "Please ask your policy-related question."
    elif selected_option == "back":
        keyboard = [
            [InlineKeyboardButton("FAQs", callback_data="faqs")],
            [InlineKeyboardButton("Placement Information", callback_data="placement")],
            [InlineKeyboardButton("Company Information", callback_data="company")],
            [InlineKeyboardButton("Statistics", callback_data="statistics")],
            [InlineKeyboardButton("Preparation Tips", callback_data="preparation")],
            [InlineKeyboardButton("Internship Information", callback_data="internship")],
            [InlineKeyboardButton("Policies", callback_data="policies")]
        ]
        response_text = "Main Menu:"
    else:
        keyboard = []
        response_text = "Invalid selection."

    if selected_option == "policy_6":
        await query.edit_message_text(text=response_text)
    else:
        await query.edit_message_text(text=response_text, reply_markup=InlineKeyboardMarkup(keyboard))

# Message handler for OTP authentication and policy questions
async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    state = context.user_data.get("state")

    if state == "WAITING_FOR_EMAIL":
        await handle_email(update, context)
    elif state == "WAITING_FOR_OTP":
        await handle_otp(update, context)
    elif state == "WAITING_FOR_POLICY_QUESTION":
        await handle_policy_question(update, context)
    elif state == "READY_TO_ASSIST":
        await handle_query(update, context)
    else:
        await update.message.reply_text("Please use the /start command to begin.")

# Use sync_to_async for the send_otp function
async_send_otp = sync_to_async(send_otp)

async def handle_email(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    email = update.message.text
    if re.match(r"[^@\s]+@mc\.vjti\.ac\.in$", email):
        otp = await async_send_otp(email)
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
        user_otp = int(user_otp)
    except ValueError:
        await update.message.reply_text("Invalid OTP format. Please enter a numeric OTP.")
        return

    if context.user_data.get("otp") == user_otp:
        context.user_data["state"] = "READY_TO_ASSIST"
        keyboard = [
            [InlineKeyboardButton("FAQs", callback_data="faqs")],
            [InlineKeyboardButton("Placement Information", callback_data="placement")],
            [InlineKeyboardButton("Company Information", callback_data="company")],
            [InlineKeyboardButton("Statistics", callback_data="statistics")],
            [InlineKeyboardButton("Preparation Tips", callback_data="preparation")],
            [InlineKeyboardButton("Internship Information", callback_data="internship")],
            [InlineKeyboardButton("Policies", callback_data="policies")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("Authentication successful! Please choose an option to proceed:", reply_markup=reply_markup)
    else:
        await update.message.reply_text("Invalid OTP. Please try again.")


        
@sync_to_async
def get_cohere_response(query):
    try:
        # Fetch all PolicyFAQ entries to provide broader context
        policy_faqs = PolicyFAQ.objects.filter(
        Q(question__icontains=query) | Q(answer__icontains=query) | Q(keywords__icontains=query))[:5]  # Limit to the top 5 entries

        faq_list = list(policy_faqs)
        
        if faq_list:
            context = "\n".join([f"Q: {faq.question} A: {faq.answer}" for faq in faq_list])
        else:
            context = ""
        
        if not context:
            return "No policy data available in the database."
        
        # Use Cohere to generate a response based on the full context
        response = cohere_client.generate(
            model="command",
            prompt=(
                f"Given the following policy FAQs:\n{context}\n\n"
                f"Please answer the following question in a clear and detailed manner:\n'{query}'\n\nAnswer:"
            ),
            max_tokens=90,
            temperature=0.7,
            k=0,
            stop_sequences=[],
            return_likelihoods="NONE",
        )
        
        if response and response.generations:
            return response.generations[0].text.strip()
        else:
            return "I couldn't generate a response at the moment. Please try again."
    
    except Exception as e:
        logger.error(f"Error fetching response: {e}")
        return "Sorry, I couldn't process your request at the moment."



async def handle_policy_question(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text
    if user_message.lower() == "/back":
        context.user_data["state"] = "READY_TO_ASSIST"
        await update.message.reply_text("Back to Main Menu. Please choose an option to proceed:")
    else:
        cohere_response = await get_cohere_response(user_message)
        await update.message.reply_text(cohere_response)
        await update.message.reply_text("Please ask another policy-related question or type '/back' to return to the main menu.")

async def handle_query(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text.lower()

    if user_message == "menu":
        keyboard = [
            [InlineKeyboardButton("FAQs", callback_data="faqs")],
            [InlineKeyboardButton("Placement Information", callback_data="placement")],
            [InlineKeyboardButton("Company Information", callback_data="company")],
            [InlineKeyboardButton("Statistics", callback_data="statistics")],
            [InlineKeyboardButton("Preparation Tips", callback_data="preparation")],
            [InlineKeyboardButton("Internship Information", callback_data="internship")],
            [InlineKeyboardButton("Policies", callback_data="policies")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("Main Menu:", reply_markup=reply_markup)
        return

    await update.message.reply_text("Invalid option! Please type 'Menu' to select a valid option.")

def main():
    application = Application.builder().token(settings.TELEGRAM_BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
    application.run_polling()

if __name__ == '__main__':
    main()