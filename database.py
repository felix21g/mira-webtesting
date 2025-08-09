# In database.py
import firebase_admin
from firebase_admin import credentials, firestore
import uuid
from datetime import datetime, timezone
from dotenv import load_dotenv
import os 
import streamlit as st

load_dotenv()

# Initialize Firestore
service_account_file = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
if not service_account_file:
    st.error("Error: GOOGLE_APPLICATION_CREDENTIALS environment variable is not set. Please add it to your .env file or Streamlit secrets.")
    st.stop() # Stops the app from running further

try:
    # Use os.path.join to create a robust file path
    service_account_key_path = os.path.join(os.getcwd(), service_account_file)
    cred = credentials.Certificate(service_account_key_path)

    if not firebase_admin.apps:
        firebase_admin.initialize_app(cred)
    
    db = firestore.client()
    print("Firebase Admin SDK initialized successfully.")

except Exception as e:
    st.error(f"Error initializing Firebase Admin SDK: {e}")
    st.stop() # Stops the app if initialization fails

def save_chat_history(session_id, user_message, bot_message):
    """Saves a turn of conversation to Firestore."""
    try:
        doc_ref = db.collection("chat_sessions").document(session_id).collection("messages").document()
        doc_ref.set({
            "user_message": user_message,
            "bot_message": bot_message,
            "timestamp": datetime.now(timezone.utc)
        })
        print(f"History saved for session {session_id}")
    except Exception as e:
        print(f"Error saving to Firestore: {e}")

def get_chat_history(session_id):
    """Returns chat history formatted for OpenAI API."""
    messages_ref = db.collection("chat_sessions").document(session_id).collection("messages")
    try:
        docs = messages_ref.order_by("timestamp").stream()
        chat_history = []

        for doc in docs:
            data = doc.to_dict()
            if "user_message" in data:
                chat_history.append({"role": "user", "content": data["user_message"]})
            if "bot_message" in data:
                chat_history.append({"role": "assistant", "content": data["bot_message"]})

        return chat_history
    except Exception as e:
        print(f"Error fetching chat history: {e}")
        return []