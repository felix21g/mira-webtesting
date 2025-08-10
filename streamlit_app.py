import streamlit as st
import uuid
import sys
import os

# --- Import both chatbot modules with aliases ---
# Assuming your chatbot_warm.py and chatbot_clinical.py files are in a sibling folder
# or accessible via the Python path. Adjust the path below if needed.
# If they are in the same directory as this streamlit_app.py, you can just use `from chatbot_warm import...`.

# Example if chatbot files are in a 'chatbot_services' folder:
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'chatbot_types')))

from chatbot_types.chatbot_warm import get_chatbot_response as get_warm_response
from chatbot_types.chatbot_clinical import get_chatbot_response as get_clinical_response

# --- Import the database functions ---
# Assuming database.py is in the same directory
from database import save_chat_history, get_chat_history

# --- Streamlit UI Configuration ---
st.set_page_config(page_title="MIRA Chatbot Persona Testing", layout="wide")
st.title("🤖 MIRA Chatbot Persona Tester")
st.markdown("Use the selector below to switch between the **Warm** and **Clinical** chatbot personas.")

# --- Added Instructions for Testers ---
st.markdown("""
Welcome to our caregiver support chatbot study. Your participation is vital in helping us understand how to provide the best possible assistance to caregivers.

### Your Primary Task

**Your goal is to find guidance on how to calm an agitated person with dementia.**

**Instructions:**
1.  **Select a Persona:** Use the radio button below to choose a chatbot persona to interact with.
2.  **Seek Information:** Use the chat box to ask for help with the primary task. You can ask questions like, "How can I calm my agitated father?" or "What are some strategies for managing agitation in dementia?"
3.  **Find the Answer:** Continue the conversation until the chatbot provides a clear, actionable list of strategies for calming agitation.
4.  **Provide Feedback:** After completing the task, you will be asked to rate your trust in the chatbot.

Thank you for your valuable contribution to this study.
""")


# --- Persona Selector ---
# This widget is used to select the chatbot persona for the session.
selected_persona = st.radio(
    "Select Chatbot Persona:",
    ("warm", "clinical"),
    index=0,  # Default to 'warm'
    help="Choosing a persona will clear the current chat history to start fresh."
)

# --- Session State Management ---
# This is crucial for maintaining chat history across user interactions.
# We reset the history and session ID if the persona is changed.
if "session_id" not in st.session_state or st.session_state.get("current_persona") != selected_persona:
    st.session_state.session_id = str(uuid.uuid4())
    # We will let the backend handle prepending the SYSTEM_PROMPT for each turn.
    st.session_state.messages = [] 
    st.session_state.current_persona = selected_persona
    st.success(f"Starting a new conversation with the **{selected_persona}** persona.")

# --- Display Chat History ---
# Iterate through the stored messages and display them.
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Chat Input ---
# This block handles user input and chatbot responses.
if user_input := st.chat_input("How can I help you today?"):
    # 1. Add user message to session state and display it
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # 2. Get chatbot response based on the selected persona
    with st.spinner(f"Thinking as a {selected_persona} chatbot..."):
        # Construct the chat history from the session state.
        # The user's new message is already appended to st.session_state.messages.
        chat_history = st.session_state.messages

        # Call the correct get_chatbot_response function based on the radio button selection
        if selected_persona == "warm":
            bot_response = get_warm_response(chat_history=chat_history)
        else: # selected_persona == "clinical"
            bot_response = get_clinical_response(chat_history=chat_history)

    # 3. Display bot response
    with st.chat_message("assistant"):
        st.markdown(bot_response)

    # 4. Add bot response to session state
    st.session_state.messages.append({"role": "assistant", "content": bot_response})
    
    # 5. Save the conversation turn to Firestore
    save_chat_history(
        session_id=st.session_state.session_id,
        user_message=user_input,
        bot_message=bot_response
    )
    
    # 6. Rerun the app to display new messages
    st.rerun()
