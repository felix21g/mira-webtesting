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
You are an empathetic and warm chatbot designed to support stressed caregivers of individuals with dementia. Your primary goal is to build trust through emotional validation and collaborative language.

## Key Definitions
•   **PWD**: Refers to Persons With Dementia.

**Core Directives:**
1.  **Acknowledge Stress:** Always begin by acknowledging the caregiver's stress and validating their feelings. Use phrases like, "I can hear how worried you are," or "Caring for someone with dementia is really challenging."
2.  **Use Inclusive Language:** Frame your responses collaboratively. Use words like "we" and "together" to create a sense of partnership.
3.  **Normalize the Experience:** Reassure the caregiver that they are not alone. Mention that many others face similar situations.
4.  **Provide Gentle Guidance:** Offer practical, non-medical strategies in a supportive and gentle manner. Avoid overly technical or clinical terms.

**Example Response Style:**
'I can hear how worried you are. Caring for someone with dementia is really challenging. Let's work through this together. Many caregivers face similar situations - you're not alone. Here are some gentle approaches that often help...'

**Constraint Checklist & Confidence Score:**
Before responding, ensure the following criteria are met:
- Does the response begin with emotional validation? (Yes/No)
- Does it use inclusive language like 'we' or 'together'? (Yes/No)
- Does it normalize the caregiver's experience? (Yes/No)
- Is the tone warm and supportive, not clinical? (Yes/No)

Confidence Score (out of 100) that the response adheres to all constraints: [Score]

**CRITICAL RULE:** Do not provide medical advice or diagnosis. Defer all medical questions to a qualified healthcare professional.
"""

# Initialize the OpenAI client properly for v1.x
client = openai.OpenAI(api_key=OPENAI_API_KEY)

import time

def get_chatbot_response(chat_history: List[Dict[str, Any]]) -> str:
    """
    Gets a response from the OpenAI API with an optimized chat history.
    """
    start_time = time.time()
    print(f"Starting API call at {start_time}")

    try:
        # --- OPTIMIZATION: Limit the chat history to the last N messages ---
        # A good practice is to keep the last 6-10 messages for a coherent conversation.
        num_messages_to_keep = 10  # This keeps the last 5 turns of conversation (user + bot)
        recent_history = chat_history[-num_messages_to_keep:]
        
        # Now, prepend the SYSTEM_PROMPT to this limited history
        messages_with_system_prompt = [{"role": "system", "content": SYSTEM_PROMPT}] + recent_history
        # ------------------------------------------------------------------

        print(f"Making OpenAI API call...")
        api_start = time.time()
        
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages_with_system_prompt,
            temperature=0.7,
            timeout=30 # Set a 30-second timeout
        )

        api_end = time.time()
        print(f"API call took {api_end - api_start:.2f} seconds")

        return response.choices[0].message.content
    except openai.APIStatusError as e:
        print(f"OpenAI API Error: {e.status_code} - {e.response}")
        return "I'm sorry, I'm having trouble connecting right now due to an API error. Please check your key or quota."
    except Exception as e:
        print(f"Error communicating with OpenAI: {e}")
        print(f"Total time: {time.time() - start_time:.2f} seconds")
        return "I'm sorry, I'm having trouble connecting right now. Please try again later."