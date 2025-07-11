import requests
import json

# Set your Cohere API key
API_KEY = "8CsCDBsCyyDQriHfwCj0AAz3sGRF66szhdxt75fw"
API_URL = "https://api.cohere.ai/v1/generate"

def check_cohere_api():
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "command",
        "prompt": "Say 'Hello, World!'",
        "max_tokens": 10
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        if response.status_code == 200:
            print("✅ Cohere API is active and responding.")
            print("Response:", response.json())
        elif response.status_code == 401:
            print("❌ Invalid API Key. Check your API key.")
        else:
            print(f"⚠️ API returned status code: {response.status_code}")
            print("Response:", response.json())
    except Exception as e:
        print("❌ Error connecting to Cohere API:", str(e))

check_cohere_api()
