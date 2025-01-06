from app.api_call import get_chatgpt_response
from app.systemprompts import SYSTEM_PROMPTS  # Import the prompts

def generate_answer(messages, history=None, mode=None, api_key=None):
    # Initialize conversation with system prompt
    conversation = []

    print(f"Debug - Received API key in generate_answer: {api_key[:8] if api_key else None}")  # Debug log
    print(f"Debug - Received mode: {mode}")  # Debug log
    print(f"Debug - Available modes: {list(SYSTEM_PROMPTS.keys())}")  # Debug log

    # Add system message based on mode
    if mode and mode in SYSTEM_PROMPTS:
        system_message = {"role": "system", "content": SYSTEM_PROMPTS[mode]}
        conversation.append(system_message)
        print(f"Debug - Added system prompt for mode: {mode}")
    else:
        print(f"Debug - Invalid mode: {mode}")
    
    # Add conversation history if provided
    if history:
        conversation.extend(history)
    
    # Add the current user message
    if messages and messages[-1]["role"] == "user":
        conversation.append(messages[-1])
    
    # Log the full conversation for debugging
    print("Full conversation context:", conversation)
    
    if not api_key:
        raise ValueError("No API key provided to generate_answer")
    
    # Pass api_key to get_chatgpt_response
    answer = get_chatgpt_response(conversation, api_key)
    return answer