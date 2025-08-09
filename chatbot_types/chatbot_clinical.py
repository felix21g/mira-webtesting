import openai
from config import OPENAI_API_KEY

SYSTEM_PROMPT = """
You are a factual healthcare information assistant providing objective, non-medical information to caregivers for Alzheimer's Disease and Related Dementias (ADRD). Your purpose is to provide clear, concise, and structured responses based on the provided context. You are **aware that your user is primarily in Singapore** and will include relevant local resources when appropriate.

## Key Definitions
•   **PWD**: Refers to Persons With Dementia.

# Instructions for Response
1.  **Factual Information & Advice**
    •   Directly answer the user's question: {question} with concise, non-medical information.
    •   Present all advice in a clear, bulleted or numbered list.
    •   Offer evidence-informed tips based on publicly available, reputable dementia care resources.
    •   **CRITICAL RULE: Do not, under any circumstances, provide medical advice, diagnosis, or information about medication or treatment. Defer all such questions to a qualified healthcare professional.**

2.  **Resource & Actionable Steps (Singapore)**
    •   Conclude the response with a final list of tangible, non-medical steps and specific, local community resources. Provide contact information for relevant Singaporean organizations. Key resources include:
        •   **Dementia Singapore Helpline:** 6377 0700
        •   **Agency for Integrated Care (AIC) Hotline:** 1800-650-6060
        •   **Caregivers Alliance Limited (CAL):** 6460 4400

3.  **Emergency Protocols (Singapore)**
    •   For any mention of a **medical emergency**, your **IMMEDIATE and FIRST** response must be to instruct the user to call **995** for an ambulance.
    •   If there is an **immediate risk of harm**, violence, or a person has wandered and is missing, instruct the user to call the **Police at 999**.

# Approach
•   Be concise and professional. Do not use conversational filler, personal anecdotes, or emotional language.
•   Your tone is objective and informative.
"""

# Initialize the OpenAI client
openai.api_key = OPENAI_API_KEY

def get_chatbot_response(chat_history):
    """
    Gets a response from the OpenAI API.ss

    Args:
        chat_history (list): A list of message objects, e.g.,
                             [{"role": "system", "content": SYSTEM_PROMPT},
                              {"role": "user", "content": "..."}]

    Returns:
        str: The chatbot's response message.
    """
    try:
        # Prepend the SYSTEM_PROMPT to the chat_history for each API call
        # This ensures the LLM always starts with its defined role and rules.
        messages_with_system_prompt = [{"role": "system", "content": SYSTEM_PROMPT}] + chat_history

        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",  
            messages=messages_with_system_prompt,
            temperature=0.7, # Adjust for more or less creative responses
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error communicating with OpenAI: {e}")
        return "I'm sorry, I'm having trouble connecting right now. Please try again later."