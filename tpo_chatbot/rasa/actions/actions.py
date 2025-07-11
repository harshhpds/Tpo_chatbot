import os
import sys
import django
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from asgiref.sync import sync_to_async


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tpo_chatbot.settings")
django.setup()
from chatbot.models import PolicyFAQ
# Load Sentence Transformer model (use same as in bot.py)
sbert_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# Cache policy data
policy_questions = []
policy_answers = {}
policy_embeddings = None
index = None  # FAISS index


async def load_policies():
    global policy_questions, policy_answers, policy_embeddings, index
    policies = await sync_to_async(lambda: list(PolicyFAQ.objects.all()))()

    if policies:
        policy_questions = [policy.question for policy in policies]
        policy_answers = {policy.question: policy.answer for policy in policies}
        
        # Encode policies with SBERT
        policy_embeddings = sbert_model.encode(policy_questions, convert_to_numpy=True)
        
        # Build FAISS index
        index = faiss.IndexFlatL2(policy_embeddings.shape[1])
        index.add(policy_embeddings)


class ActionFetchPolicy(Action):
    def name(self) -> Text:
        return "action_fetch_policy"

    async def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        if index is None:
            await load_policies()  # Ensure policies are loaded

        user_query = tracker.latest_message.get("text")
        query_embedding = sbert_model.encode([user_query], convert_to_numpy=True)

        # FAISS similarity search
        D, I = index.search(query_embedding, 1)
        best_match = policy_questions[I[0][0]] if D[0][0] < 1.0 else None

        if best_match:
            response = policy_answers[best_match]
        else:
            response = "I'm sorry, I couldn't find an exact answer. Please check the placement policies or contact the TPO."

        dispatcher.utter_message(text=response)
        return []
