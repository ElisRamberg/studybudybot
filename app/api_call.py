from openai import OpenAI
import os

def get_chatgpt_response(messages, api_key):
    try:
        if not api_key:
            raise ValueError("No API key provided")
            
        print(f"Using API key: {api_key[:8]}...") # Only print first 8 chars for security
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            stream=True
        )
        print("Got response from OpenAI")  # Debug log
        
        for chunk in response:
            print(f"Processing chunk: {chunk}")  # Debug log
            if chunk and chunk.choices and chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
                
    except Exception as e:
        print(f"Error in get_chatgpt_response: {str(e)}")
        import traceback
        print(traceback.format_exc())
        raise  # Re-raise the exception to be handled by the caller