# In database.py
import firebase_admin
from firebase_admin import credentials, firestore, apps
import uuid
from datetime import datetime, timezone
import streamlit as st



# Check if Firebase credentials are provided in Streamlit's secrets
@st.cache_resource
def get_firestore_client():
    if "firebase" not in st.secrets:
        st.error("Firebase credentials not found in Streamlit secrets.")
        st.stop()
        
    try:
        cred_dict = dict(st.secrets["firebase"])
        cred = credentials.Certificate(cred_dict)
        
        # Check if the app is already initialized, just in case
        if not firebase_admin.apps:
            firebase_admin.initialize_app(cred)
        
        return firestore.client()
        print("Firebase Admin SDK initialized successfully.")
    except Exception as e:
        st.error(f"Error initializing Firebase Admin SDK: {e}")
        st.stop()

db = get_firestore_client()

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