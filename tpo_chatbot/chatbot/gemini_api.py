import asyncio
import sys
import os
import re
import django
import logging
import random
import smtplib
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from asgiref.sync import sync_to_async
from django.conf import settings
import google.generativeai as genai
from django.db.models import Q  # Correct import for Q object
import numpy as np
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Set up Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tpo_chatbot.settings")
django.setup()

from chatbot.models import FAQ, CompanyInfo, Internship, PlacementStatistics, PolicyFAQ, Role, Student, PlacementRecord,Document

# Initialize Gemini API client (Cohere client removed)
genai.configure(api_key="AIzaSyCpjHqW6t4oSg1Ge_zYcag854fqGVYwdXA")  # Replace with your actual API key

# Function to send OTP via email
def send_otp(email):
    otp = random.randint(100000, 999999)
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = "harsh.hpds@gmail.com"
    sender_password = "fqhcumomzvqtvgoy"

    subject = "OTP for TPO Chatbot Authentication - VJTI TPO Team"
    body = f"""\
<html>
<body style="font-family: Arial, sans-serif; color: #333;">
    <p>Dear Student,</p>
    <p>Your One-Time Password (OTP) for accessing the VJTI TPO Chatbot has been generated.</p>
    <p>Please use the OTP provided below to complete your authentication:</p>
    <p style="font-size: 18px;"><b><span style="color: black;">{otp}</span></b></p>
    <p>This OTP is valid for <b>5 minutes</b>. If you did not request this authentication, please ignore this email or contact the TPO Team immediately.</p>
    <p>Thank you for choosing VJTI TPO Services.</p>
    <p><b>Best regards,</b><br>VJTI TPO Team</p>
</body>
</html>
"""
    msg = MIMEMultipart()
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = email
    msg.attach(MIMEText(body, "html"))  # Using HTML format for rich text

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
            [InlineKeyboardButton("Download a list of all companies", callback_data="company_3")],
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
    elif selected_option == "faq_1":
        await query.edit_message_text(text="TPO office hours: 10am-5pm\n\nor type '/back' to return to the main menu.")
        return
    elif selected_option == "faq_2":
        await query.edit_message_text(text="How can I contact the TPO?\nYou can email at tpo@gmail.com or visit the office.\n\nor type '/back' to return to the main menu.")
        return
    elif selected_option == "faq_3":
        await query.edit_message_text(text="The head of the TPO department is: xyz.\n\nor type '/back' to return to the main menu.")
        return
    elif selected_option == "faq_4":
        await query.edit_message_text(text="The TPO office is located in the college.\n\nor type '/back' to return to the main menu.")
        return
    elif selected_option == "company_1":
        # Set state to ask for company name to fetch detailed info
        context.user_data["state"] = "READY_TO_ASSIST_COMPANY_INFO"
        await query.edit_message_text(text="Please enter the company name to get detailed information (including recent projects and all important details), or type '/back' to return to the main menu.")
        return
    elif selected_option == "company_2":
        # Set state to ask for company name to fetch selection process info
        context.user_data["state"] = "READY_TO_ASSIST_SELECTION"
        await query.edit_message_text(text="Please enter the company name to get details about its selection process, or type '/back' to return to the main menu.")
        return
    
    elif selected_option == "company_3":
        try:
            company_doc = await get_latest_company_doc()  # Fetch asynchronously

            if company_doc.file:
                file_path = os.path.join(settings.MEDIA_ROOT, company_doc.file.name)  # Correct file path

                with open(file_path, "rb") as file:
                    await context.bot.send_document(
                        chat_id=query.message.chat_id,
                        document=file,
                        caption="Here is the latest list of all companies.\n\nType '/back' to return to the main menu."
                    )
                await query.edit_message_text(text="The company list has been sent to you.\n\ntype '/back' to return to the main menu.")
            else:
                await query.edit_message_text(text="No company list is available at the moment. Please try again later.")

        except Document.DoesNotExist:
            await query.edit_message_text(text="No company list is available at the moment. Please try again later.")

        return
    
    elif selected_option == "policy_6":
        # Trigger Gemini for "Other Policy Questions"
            if "branch" not in context.user_data:
                    keyboard = [
                        [InlineKeyboardButton("Computer Science", callback_data="dept_cs")],
                        [InlineKeyboardButton("Mechanical", callback_data="dept_mech")],
                        [InlineKeyboardButton("Electrical", callback_data="dept_elec")],
                        [InlineKeyboardButton("Civil", callback_data="dept_civil")],
                        [InlineKeyboardButton("Production", callback_data="dept_prod")],
                        [InlineKeyboardButton("Electronics", callback_data="dept_elec")],
                        [InlineKeyboardButton("Telecommunication (EXTC)", callback_data="dept_telecom")],
                        [InlineKeyboardButton("MCA", callback_data="dept_mca")],
                        [InlineKeyboardButton("Mtech CS", callback_data="dept_mtech_cs")],
                        [InlineKeyboardButton("Mtech IT", callback_data="dept_mtech_it")],
                        [InlineKeyboardButton("Other", callback_data="dept_other")]
                        ]
                    reply_markup = InlineKeyboardMarkup(keyboard)
                    await query.edit_message_text("Please select your branch:", reply_markup=reply_markup)
                    return

        # Ask for CGPA
            keyboard = [
                [InlineKeyboardButton("Enter CGPA", callback_data="enter_cgpa")],
                [InlineKeyboardButton("Not Applicable", callback_data="cgpa_na")]
            ]   
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text("Please provide your CGPA for the 1st and 2nd semesters:", reply_markup=reply_markup)
            return

    elif selected_option.startswith("dept_"):
        # Save branch
        context.user_data["branch"] = selected_option.split("_")[1]
        keyboard = [
            [InlineKeyboardButton("Enter CGPA", callback_data="enter_cgpa")],
            [InlineKeyboardButton("Not Applicable", callback_data="cgpa_na")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("branch recorded. Please provide your CGPA for the 1st and 2nd semesters:", reply_markup=reply_markup)
        return

    elif selected_option == "enter_cgpa":
        context.user_data["state"] = "WAITING_FOR_CGPA"
        await query.edit_message_text("Please enter your CGPA (e.g., 8.5).")
        return

    elif selected_option == "cgpa_na":
        context.user_data["cgpa"] = "Not Applicable"
        keyboard = [
            [InlineKeyboardButton("Yes", callback_data="study_yes")],
            [InlineKeyboardButton("No", callback_data="study_no")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("Are you planning to apply for further studies?", reply_markup=reply_markup)
        return

    elif selected_option == "study_yes":
        context.user_data["further_study"] = "Yes"
        context.user_data["state"] = "WAITING_FOR_POLICY_QUESTION"
        await query.edit_message_text("Please ask your policy-related question.")
        return

    elif selected_option == "study_no":
        context.user_data["further_study"] = "No"
        context.user_data["state"] = "WAITING_FOR_POLICY_QUESTION"
        await query.edit_message_text("Please ask your policy-related question.")
        return
    
    elif selected_option == "back":
        await back_command(update, context)  # ✅ Calls back_command() so it matches OTP menu
        return

    else:
        keyboard = []
        response_text = "Invalid selection."

    await query.edit_message_text(text=response_text, reply_markup=InlineKeyboardMarkup(keyboard))

# Message handler for OTP authentication, policy questions, and company queries
async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text.strip().lower()

    # ✅ Ensure "/back" or "menu" resets the state and sends the main menu
    if user_message in ["/back", "menu"]:
        context.user_data["state"] = "READY_TO_ASSIST"  # Reset state to main menu
        keyboard = [
            [InlineKeyboardButton("FAQs", callback_data="faqs")],
            #[InlineKeyboardButton("Placement Information", callback_data="placement")],
            [InlineKeyboardButton("Company Information", callback_data="company")],
            [InlineKeyboardButton("Statistics", callback_data="statistics")],
            [InlineKeyboardButton("Preparation Tips", callback_data="preparation")],
            #[InlineKeyboardButton("Internship Information", callback_data="internship")],
            [InlineKeyboardButton("Policies", callback_data="policies")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("Main Menu:", reply_markup=reply_markup)
        return  # Stop further processing

    # ✅ Handle different bot states
    state = context.user_data.get("state", "READY_TO_ASSIST")

    if state == "WAITING_FOR_EMAIL":
        await handle_email(update, context)
    elif state == "WAITING_FOR_OTP":
        await handle_otp(update, context)
    elif state == "WAITING_FOR_POLICY_QUESTION":
        await handle_policy_question(update, context)
    elif state == "READY_TO_ASSIST_COMPANY_INFO":
        await handle_company_info(update, context)
    elif state == "READY_TO_ASSIST_SELECTION":
        await handle_company_selection(update, context)
    elif state == "WAITING_FOR_CGPA":
        try:
            cgpa = float(user_message)
            context.user_data["cgpa"] = cgpa
            keyboard = [
                [InlineKeyboardButton("Yes", callback_data="study_yes")],
                [InlineKeyboardButton("No", callback_data="study_no")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text("CGPA recorded. Are you planning to apply for further studies?", reply_markup=reply_markup)
        except ValueError:
            await update.message.reply_text("Invalid CGPA format. Please enter a numeric value (e.g., 8.5).")
        return
    else:
        await update.message.reply_text("Invalid option! Please type '/back' to go to the main menu.")



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
            #[InlineKeyboardButton("Placement Information", callback_data="placement")],
            [InlineKeyboardButton("Company Information", callback_data="company")],
            [InlineKeyboardButton("Statistics", callback_data="statistics")],
            [InlineKeyboardButton("Preparation Tips", callback_data="preparation")],
            #[InlineKeyboardButton("Internship Information", callback_data="internship")],
            [InlineKeyboardButton("Policies", callback_data="policies")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("Authentication successful! Please choose an option to proceed:", reply_markup=reply_markup)
    else:
        await update.message.reply_text("Invalid OTP. Please try again.")

# Function to get Gemini response for company info (detailed information including recent projects)
async def get_company_info(company_name: str) -> str:
    prompt = f"""
    Provide a **concise** summary of {company_name}, including:
    - Key details (industry, headquarters)
    - Recent projects (if available)
    - Any useful info for students

    Limit response to **300 words maximum**.
    """

    try:
        model = genai.GenerativeModel("gemini-1.5-pro-latest")
        response = model.generate_content(prompt)
        return response.text.strip() if response and response.text else "Company details not available."
    except Exception as e:
        return f"Error fetching company info: {str(e)}"


# Function to get Gemini response for selection process info

async def get_company_selection(company_name: str) -> str:
    prompt = f"Provide detailed information about the selection process for the company {company_name}. Limit response to **300 words maximum**  "
    model = genai.GenerativeModel("gemini-1.5-pro-latest")
    
    for attempt in range(5):  # Retry up to 5 times
        try:
            response = model.generate_content(prompt)
            if response and response.text:
                return response.text.strip()
            else:
                return "I couldn't fetch the selection process information at the moment."
        except Exception as e:
            if "429" in str(e):
                wait_time = 2 ** attempt  # Exponential backoff
                print(f"Rate limit exceeded. Retrying in {wait_time} seconds...")
                await asyncio.sleep(wait_time)
            else:
                return f"Error fetching selection process info: {str(e)}"
    return "Failed to fetch company selection info after multiple attempts."


async def handle_company_info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    company_name = update.message.text.strip()

    # ✅ Handle the /back command
    if company_name.lower() == "/back":
        await message_handler(update, context)  # Call main menu function
        return

    info = await get_company_info(company_name)
    await update.message.reply_text(f"Details about {company_name}:\n\n{info}\n\nPlease enter another company name or type '/back' to return to the main menu.")
    
    # Keep the state for further company information requests
    context.user_data["state"] = "READY_TO_ASSIST_COMPANY_INFO"

async def handle_company_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    company_name = update.message.text.strip()

    # ✅ Handle the /back command
    if company_name.lower() == "/back":
        await message_handler(update, context)  # Call main menu function
        return

    info = await get_company_selection(company_name)
    await update.message.reply_text(f"Selection process for {company_name}:\n\n{info}\n\nPlease enter another company name or type '/back' to return to the main menu.")
    
    # Keep the state for further selection process requests
    context.user_data["state"] = "READY_TO_ASSIST_SELECTION"




@sync_to_async
def get_latest_company_doc():
    return Document.objects.filter(category="company_list").latest("uploaded_at")

@sync_to_async
def get_gemini_response(query, branch, cgpa, further_study):
    try:
        # Generate an embedding for the user's query using the text-embedding model
        query_embed_resp = genai.embed_content("models/text-embedding-004", content=query)
        query_embedding = query_embed_resp.get("embedding")
        if not query_embedding:
            return "Unable to generate embedding for your query."

        # Function to compute cosine similarity between two vectors
        def cosine_similarity(vec1, vec2):
            vec1 = np.array(vec1)
            vec2 = np.array(vec2)
            return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

        # Retrieve the best matching FAQ based on cosine similarity of embeddings
        best_faq = None
        best_score = -1

        for faq in PolicyFAQ.objects.all():
            if faq.embedding:
                score = cosine_similarity(query_embedding, faq.embedding)
                if score > best_score:
                    best_score = score
                    best_faq = faq

        # If no FAQ is similar enough, return a fallback message
        if best_faq is None or best_score < 0.5:
            return "No relevant policy found in the database."

        # Prepare context using the best matching FAQ
        faq_context = f"Q: {best_faq.question}\nA: {best_faq.answer}"
        
        
        # Generate a response using the Gemini generative model.
        # Use "models/gemini-1.5-flash-latest" as it is in your supported list.
        prompt = f"""Based on the following details
        Details you should know: 
        1.Core branches: Mechanical, Civil, Production, and Electrical Engineering.
        2.Circuit branches: Electronics and Telecommunication (EXTC), Electronics, and Electrical Engineering.
        3.Computer branches : MCA, CS, IT   
        (Note: Electrical Engineering is often treated under both Core and Circuit depending on context.)

        User Details:
        - branch: {branch}
        - CGPA: {cgpa}
        - Further Study Plans: {further_study}                  
              \n{faq_context}\n\nUser Query: {query}\n\nAnswer:
                          
        """
        
        model = genai.GenerativeModel("models/gemini-1.5-flash-latest")
        response = model.generate_content(prompt)
        
        if response and response.text:
            return response.text.strip()
        else:
            return "I couldn't generate a response at the moment. Please try again."
    except Exception as e:
        return f"Sorry, an error occurred: {str(e)}"

# Modify the handle_policy_question function to use get_gemini_response
async def handle_policy_question(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text.strip()

    # ✅ Handle the /back command
    if user_message.lower() == "/back":
        await message_handler(update, context)  # Call main menu function
        return
    branch = context.user_data.get("branch", "Unknown")
    cgpa = context.user_data.get("cgpa", "Not Provided")
    further_study = context.user_data.get("further_study", "Not Provided")

    # Call get_gemini_response with user details
    gemini_response = await get_gemini_response(user_message, branch, cgpa, further_study)
    await update.message.reply_text(gemini_response)
    await update.message.reply_text("Please ask another policy-related question or type '/back' to return to the main menu.")

async def back_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the /back command and returns to the main menu with the same layout as OTP authentication."""
    context.user_data["state"] = "READY_TO_ASSIST"  # Reset state to main menu

    keyboard = [
        [InlineKeyboardButton("FAQs", callback_data="faqs")],
        #[InlineKeyboardButton("Placement Information", callback_data="placement")],
        [InlineKeyboardButton("Company Information", callback_data="company")],
        [InlineKeyboardButton("Statistics", callback_data="statistics")],
        [InlineKeyboardButton("Preparation Tips", callback_data="preparation")],
        #[InlineKeyboardButton("Internship Information", callback_data="internship")],
        [InlineKeyboardButton("Policies", callback_data="policies")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.message:  
        # ✅ /back command from user typing
        await update.message.reply_text("You have returned to the Main Menu. Please choose an option to proceed:", reply_markup=reply_markup)
    elif update.callback_query:
        # ✅ "Back" button click
        query = update.callback_query
        await query.answer()  
        await query.edit_message_text("You have returned to the Main Menu. Please choose an option to proceed:", reply_markup=reply_markup)

async def handle_query(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text.lower()
    if user_message in ["menu", "/back"]:
        keyboard = [
            [InlineKeyboardButton("FAQs", callback_data="faqs")],
           # [InlineKeyboardButton("Placement Information", callback_data="placement")],
            [InlineKeyboardButton("Company Information", callback_data="company")],
            [InlineKeyboardButton("Statistics", callback_data="statistics")],
            [InlineKeyboardButton("Preparation Tips", callback_data="preparation")],
            #[InlineKeyboardButton("Internship Information", callback_data="internship")],
            [InlineKeyboardButton("Policies", callback_data="policies")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("Main Menu:", reply_markup=reply_markup)
        return
    await update.message.reply_text("Invalid option! Please type 'Menu' to select a valid option.")

def main():
    application = Application.builder().token(settings.TELEGRAM_BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("back", back_command))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
    application.run_polling()

if __name__ == '__main__':
    main()
