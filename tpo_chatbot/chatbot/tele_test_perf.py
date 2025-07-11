import sys
import django
from django.conf import settings
import faiss
import numpy as np
import nltk
nltk.download('punkt_tab')
import spacy
import logging
import os
import requests
from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer
from transformers import T5Tokenizer, T5ForConditionalGeneration
from asgiref.sync import sync_to_async
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackContext

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tpo_chatbot.settings")
django.setup()

from chatbot.models import PolicyFAQ

# Load NLP models
nlp = spacy.load("en_core_web_sm")
sbert_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
flan_t5_model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-small")
flan_t5_tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-small")

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Rasa API
RASA_URL = "http://localhost:5005/webhooks/rest/webhook"

async def call_rasa(query):
    """ Calls Rasa API and returns the response """
    response = requests.post(RASA_URL, json={"sender": "user", "message": query})
    rasa_data = response.json()
    
    if rasa_data:
        response_text = rasa_data[0].get("text", "")
        confidence = rasa_data[0].get("confidence", 0.0)
        return response_text, confidence
    return None, 0.0

# Fetch FAQs from the database
@sync_to_async
def fetch_faqs():
    faqs = PolicyFAQ.objects.all()
    faq_data = [{"question": faq.question, "answer": faq.answer} for faq in faqs]
    return faq_data

# Preprocess FAQs for BM25 and FAISS
async def preprocess_faqs():
    faq_data = await fetch_faqs()
    faq_questions = [faq["question"] for faq in faq_data]
    faq_answers = {faq["question"]: faq["answer"] for faq in faq_data}
    
    tokenized_corpus = [nltk.word_tokenize(q.lower()) for q in faq_questions]
    bm25 = BM25Okapi(tokenized_corpus)
    
    faq_embeddings = sbert_model.encode(faq_questions, convert_to_numpy=True)
    index = faiss.IndexFlatL2(faq_embeddings.shape[1])
    index.add(faq_embeddings)
    
    return faq_questions, faq_answers, bm25, index

# Handle messages
async def handle_message(update: Update, context: CallbackContext):
    user_query = update.message.text

    # Try Rasa first
    rasa_response, confidence = await call_rasa(user_query)
    if confidence > 0.7:
        await update.message.reply_text(rasa_response)
        return

    # Otherwise, use FAISS/BM25
    faq_questions, faq_answers, bm25, index = await preprocess_faqs()
    
    query_embedding = sbert_model.encode([user_query], convert_to_numpy=True)
    D, I = index.search(query_embedding, 1)
    best_match = faq_questions[I[0][0]] if D[0][0] < 1.0 else None

    response = faq_answers[best_match] if best_match else "I'm not sure about that. Please check the TPO portal."
    
    await update.message.reply_text(response)

# Setup bot
app = ApplicationBuilder().token(settings.TELEGRAM_BOT_TOKEN).build()
app.add_handler(CommandHandler("start", handle_message))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

app.run_polling()
