import os
import sys
import django
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from asgiref.sync import sync_to_async
from chatbot.models import PolicyFAQ

# Ensure Django is properly loaded
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tpo_chatbot.settings")
django.setup()

class ActionFetchPolicy(Action):
    def name(self) -> Text:
        return "action_fetch_policy"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        user_query = tracker.latest_message.get("text")

        # Fetch all policy questions from the database
        policies = await sync_to_async(lambda: list(PolicyFAQ.objects.all()))()

        if not policies:
            dispatcher.utter_message(text="No policy data available.")
            return []

        policy_questions = [policy.question for policy in policies]
        policy_answers = {policy.question: policy.answer for policy in policies}

        # TF-IDF Vectorization
        vectorizer = TfidfVectorizer()
        vectors = vectorizer.fit_transform(policy_questions + [user_query])
        
        user_vector = vectors[-1]  # Last vector is for user query
        policy_vectors = vectors[:-1]  # All policy vectors

        # Compute cosine similarity
        similarities = cosine_similarity(user_vector, policy_vectors).flatten()
        best_index = similarities.argmax()
        best_score = similarities[best_index]

        if best_score > 0.5:  # Threshold for relevance
            response = policy_answers[policy_questions[best_index]]
        else:
            response = "I'm sorry, I couldn't find an exact answer. Please check the placement policies or contact the TPO."

        dispatcher.utter_message(text=response)
        return []
