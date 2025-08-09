# In database.py
import firebase_admin
from firebase_admin import credentials, firestore
import uuid
from datetime import datetime, timezone

# Initialize Firestore
cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred)
db = firestore.client()

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