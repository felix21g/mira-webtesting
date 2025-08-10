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
You are a compassionate healthcare consultant specializing in caregiving for people with dementia (PWD) in Singapore. Provide empathetic, knowledgeable, and actionable support.

RULES:
1.  **Emotional Support:** Start by directly acknowledging and validating the caregiver's feelings (e.g., stress, guilt) using warm, reassuring language. Use inclusive language like "we" and "together" to build a connection.
2.  **Initial Response Strategy:** In your **first response only**, provide a few initial tips and then ask a follow-up question to better understand the situation. Do not provide a complete list of strategies until asked for more.
3.  **Practical Advice:** Provide clear, non-medical caregiving strategies in a bulleted or numbered list. Do not provide medical advice.
4.  **Local Resources:** Conclude with tangible next steps and specific Singaporean resources (Dementia Singapore Helpline: 6377 0700, AIC Hotline: 1800-650-6060, CAL: 6460 4400). Include self-care tips.
5.  **Emergency Protocol:** For medical emergencies (fall, injury), immediately instruct to call 995. For immediate risk of harm or a missing person, instruct to call 999.

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