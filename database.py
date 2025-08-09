# In database.py
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime, timezone
import streamlit as st



# Check if Firebase credentials are provided in Streamlit's secrets
cred = credentials.Certificate(dict(st.secrets["firebase"]))
# --- CHANGE THIS LINE ---
# Access the apps submodule via the main firebase_admin package
try:
    firebase_admin.initialize_app(cred)
except ValueError as e:
    # This error occurs if initialize_app() is called more than once
    # We can safely ignore it and proceed
    pass
    
db = firestore.client()
print("Firebase Admin SDK initialized successfully.")

def save_chat_history(session_id, user_message, bot_message):
    if db is None:
        print("Firestore client not initialized. Skipping save.")
        return
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
    if db is None:
        print("Firestore client not initialized. Skipping fetch.")
        return []
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