import sys
import os
import django
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from django.conf import settings

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Set up Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tpo_chatbot.settings")
django.setup()

from chatbot.models import FAQ, CompanyInfo, Internship, PlacementStatistics, Policy, PolicyFAQ, Role, Student, PlacementRecord, QuickInfo

# /start command handler: Sends the main menu inline keyboard.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("FAQs", callback_data="faqs")],
        [InlineKeyboardButton("Placement Information", callback_data="placement")],
        [InlineKeyboardButton("Company Information", callback_data="company")],
        [InlineKeyboardButton("Statistics", callback_data="statistics")],
        [InlineKeyboardButton("Preparation Tips", callback_data="preparation")],
        [InlineKeyboardButton("Internship Information", callback_data="internship")],
        [InlineKeyboardButton("Comparison", callback_data="comparison")],
        [InlineKeyboardButton("Policies", callback_data="policies")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Welcome! Please choose an option to proceed:", reply_markup=reply_markup)

# CallbackQuery handler: Processes button clicks.
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    # Get the selected option (we assume the callback_data is the same as the button text)
    selected_option = query.data

    # Step 1: Simulate that the user sent a message with the selected option.
    # (This message is sent by the bot, but appears as a separate message in the chat.)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=selected_option
    )

    # Step 2: Prepare a new inline keyboard and response text based on the selected option.
    if selected_option == "faqs":
        new_keyboard = [
            [InlineKeyboardButton("What are the TPO office hours?", callback_data="faq_1")],
            [InlineKeyboardButton("How can I contact the TPO?", callback_data="faq_2")],
            [InlineKeyboardButton("Who is the head of the TPO department?", callback_data="faq_3")],
            [InlineKeyboardButton("Where is the TPO office located?", callback_data="faq_4")],
            [InlineKeyboardButton("Back", callback_data="back")]
        ]
        response_text = "Please choose an option under FAQs:"
    elif selected_option == "placement":
        new_keyboard = [
            [InlineKeyboardButton("Which company did a specific student get placed in?", callback_data="placement_1")],
            [InlineKeyboardButton("What package was offered to a specific student?", callback_data="placement_2")],
            [InlineKeyboardButton("Back", callback_data="back")]
        ]
        response_text = "Please choose an option under Placement Information:"
    elif selected_option == "company":
        new_keyboard = [
            [InlineKeyboardButton("Tell me about a specific company", callback_data="company_1")],
            [InlineKeyboardButton("What is the selection process for a specific company?", callback_data="company_2")],
            [InlineKeyboardButton("Back", callback_data="back")]
        ]
        response_text = "Please choose an option under Company Information:"
    elif selected_option == "statistics":
        new_keyboard = [
            [InlineKeyboardButton("How many students were placed?", callback_data="statistics_1")],
            [InlineKeyboardButton("What is the average package?", callback_data="statistics_2")],
            [InlineKeyboardButton("Back", callback_data="back")]
        ]
        response_text = "Please choose an option under Statistics:"
    elif selected_option == "preparation":
        new_keyboard = [
            [InlineKeyboardButton("What are the eligibility criteria?", callback_data="preparation_1")],
            [InlineKeyboardButton("How can I prepare?", callback_data="preparation_2")],
            [InlineKeyboardButton("Back", callback_data="back")]
        ]
        response_text = "Please choose an option under Preparation Tips:"
    elif selected_option == "internship":
        new_keyboard = [
            [InlineKeyboardButton("Which internships are available?", callback_data="internship_1")],
            [InlineKeyboardButton("What is the eligibility criteria for internships?", callback_data="internship_2")],
            [InlineKeyboardButton("How can I apply for an internship?", callback_data="internship_3")],
            [InlineKeyboardButton("Back", callback_data="back")]
        ]
        response_text = "Please choose an option under Internship Information:"
    elif selected_option == "comparison":
        new_keyboard = [
            [InlineKeyboardButton("Highest package", callback_data="comparison_1")],
            [InlineKeyboardButton("Compare companies", callback_data="comparison_2")],
            [InlineKeyboardButton("Back", callback_data="back")]
        ]
        response_text = "Please choose an option under Comparison:"
    elif selected_option == "policies":
        new_keyboard = [
            [InlineKeyboardButton("What are the policies?", callback_data="policies_1")],
            [InlineKeyboardButton("Back", callback_data="back")]
        ]
        response_text = "Please choose an option under Policies:"
    elif selected_option == "back":
        # If the user clicks 'Back', show the main menu buttons again.
        new_keyboard = [
            [InlineKeyboardButton("FAQs", callback_data="faqs")],
            [InlineKeyboardButton("Placement Information", callback_data="placement")],
            [InlineKeyboardButton("Company Information", callback_data="company")],
            [InlineKeyboardButton("Statistics", callback_data="statistics")],
            [InlineKeyboardButton("Preparation Tips", callback_data="preparation")],
            [InlineKeyboardButton("Internship Information", callback_data="internship")],
            [InlineKeyboardButton("Comparison", callback_data="comparison")],
            [InlineKeyboardButton("Policies", callback_data="policies")]
        ]
        response_text = "Main Menu:"
    else:
        new_keyboard = []
        response_text = "Invalid selection."

    # Step 3: Send a new message with the response text and new inline keyboard.
    # This message will be sent as a new message, leaving the original main menu intact.
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=response_text,
        reply_markup=InlineKeyboardMarkup(new_keyboard)
    )

def main():
    application = Application.builder().token(settings.TELEGRAM_BOT_TOKEN).build()

    # Add handlers for /start and button clicks
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))

    # Run the bot
    application.run_polling()

if __name__ == '__main__':
    main()
