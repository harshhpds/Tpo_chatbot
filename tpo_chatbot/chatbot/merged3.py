import sys
import os
import django
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from asgiref.sync import sync_to_async

# Set up Django environment and settings
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tpo_chatbot.settings")
django.setup()
from django.conf import settings

import cohere

# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Load Telegram Bot Token from settings
TELEGRAM_BOT_TOKEN = settings.TELEGRAM_BOT_TOKEN

# Initialize Cohere client with fine-tuned model
cohere_client = cohere.Client(settings.COHERE_API_KEY)

# Start command: Welcomes the user.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Welcome! Ask me a policy-related question.")

# (Optional) Button handler if you want to expand functionality.
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    selected_option = query.data
    if selected_option == "policy_6":
        context.user_data["state"] = "WAITING_FOR_POLICY_QUESTION"
        await query.edit_message_text("Please ask your policy-related question.")
    else:
        await query.edit_message_text("Invalid selection.")

# Function to fetch response from your fine-tuned Cohere model.
@sync_to_async
def get_cohere_response(query):
    try:
        response = cohere_client.chat(
            model='da9268a7-a20f-452d-b944-9497a4e5742d-ft',
            #model='70d2774b-d34b-4cc7-b11a-ba47eaf80247-ft',
            message=query,
            temperature=0.5,  # Adjust temperature for a controlled response style.
            max_tokens=100    # Limit response length for conciseness.
        )
        if response and response.text:
            # Extract the first sentence for a concise answer.
            concise_response = response.text.strip().split(". ")[0]
            return concise_response if concise_response else "I couldn't generate a response."
        else:
            return "No relevant response found."
    except Exception as e:
        logger.error(f"Error fetching Cohere response: {e}")
        return "Sorry, I couldn't process your request."

# Handle policy-related questions by sending them to the fine-tuned Cohere model.
async def handle_policy_question(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text
    if user_message.lower() == "/back":
        context.user_data["state"] = "READY_TO_ASSIST"
        await update.message.reply_text("Back to Main Menu.")
    else:
        cohere_response = await get_cohere_response(user_message)
        await update.message.reply_text(cohere_response)
        await update.message.reply_text("Ask another question or type '/back' to return.")

# Main function to start the bot.
def main():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    # Command and message handlers.
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_policy_question))
    
    print("Bot is running...")
    application.run_polling()

if __name__ == "__main__":
    main()
