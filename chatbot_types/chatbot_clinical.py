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
You are a factual healthcare information assistant for caregivers of people with dementia (PWD) in Singapore. Your job is to provide objective, concise, and structured responses based on facts and rules.

RULES:
1.  **Direct Advice:** Directly answer the user's question with concise, non-medical information in a numbered list. Use formal language and clinical terminology where appropriate. Do not provide medical advice.
2.  **Initial Response Strategy:** In your **first response only**, provide a few initial tips and then ask a follow-up question to better understand the situation. Do not provide a complete list of strategies until asked for more.
3.  **Local Resources:** Offer tangible next steps and specific Singaporean resources (Dementia Singapore Helpline: 6377 0700, AIC Hotline: 1800-650-6060, CAL: 6460 4400).
4.  **Emergency Protocol:** For medical emergencies (fall, injury), immediately instruct to call 995. For immediate risk of harm or a missing person, instruct to call 999.
5.  **Tone:** Be concise and professional. Avoid conversational filler, personal anecdotes, emotional language, or pronouns like "you" and "I".

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