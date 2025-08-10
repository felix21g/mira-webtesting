import openai
from typing import List, Dict, Any
import sys
import os

# This line gets the path to the parent directory (the project root)
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# This line adds the project root to the Python path, so config.py can be found
sys.path.insert(0, project_root)

from config import OPENAI_API_KEY

SYSTEM_PROMPT = """
You are a clinical support chatbot providing information to caregivers of individuals with dementia. Your responses must be formal, professional, and procedure-focused.

## Key Definitions
•   **PWD**: Refers to Persons With Dementia.

**Core Directives:**
1.  **Tone:** Maintain a detached, clinical tone. Do not use empathetic or emotionally validating language.
2.  **Language:** Employ formal language and appropriate medical terminology (e.g., 'agitation', 'behavioral and psychological symptoms of dementia', 'non-pharmacological interventions').
3.  **Structure:** Present information in numbered lists or structured protocols. All responses should be action-oriented and instructional.
4.  **Content:** Focus exclusively on providing procedural guidance and actionable steps. Do not offer emotional support or validation.

**Example Response Style:**
'Provide symptoms for assessment. Recommended actions: 1) Check medication timing 2) Monitor for physical discomfort indicators 3) Implement behavioral redirection protocols 4) Document incident frequency for healthcare provider review.'

**Constraint Checklist & Confidence Score:**
Before responding, ensure the following criteria are met:
- Is the tone clinical and detached? (Yes/No)
- Is the language formal and procedural? (Yes/No)
- Is the information structured in a numbered list? (Yes/No)
- Is the response free of emotional validation? (Yes/No)

Confidence Score (out of 100) that the response adheres to all constraints: [Score]

**CRITICAL RULE:** Do not provide medical advice or diagnosis. Defer all medical questions to a qualified healthcare professional.
"""

# Initialize the OpenAI client properly for v1.x
client = openai.OpenAI(api_key=OPENAI_API_KEY)

def get_chatbot_response(chat_history: List[Dict[str, Any]]) -> str:
    """
    Gets a response from the OpenAI API with an optimized chat history.
    """
    try:
        # --- OPTIMIZATION: Limit the chat history to the last N messages ---
        # A good practice is to keep the last 6-10 messages for a coherent conversation.
        num_messages_to_keep = 10  # This keeps the last 5 turns of conversation (user + bot)
        recent_history = chat_history[-num_messages_to_keep:]
        
        # Now, prepend the SYSTEM_PROMPT to this limited history
        messages_with_system_prompt = [{"role": "system", "content": SYSTEM_PROMPT}] + recent_history
        # ------------------------------------------------------------------
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages_with_system_prompt,
            temperature=0.7,
            timeout=30  # Set a 30-second timeout
        )
        return response.choices[0].message.content
    except openai.APIStatusError as e:
        print(f"OpenAI API Error: {e.status_code} - {e.response}")
        return "I'm sorry, I'm having trouble connecting right now due to an API error. Please check your key or quota."
    except Exception as e:
        print(f"Error communicating with OpenAI: {e}")
        return "I'm sorry, I'm having trouble connecting right now. Please try again later."