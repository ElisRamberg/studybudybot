from openai import OpenAI
import os

client = OpenAI(api_key="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")

def get_chatgpt_response(messages, api_key):
    try:
        # Create client with provided API key
        client = OpenAI(api_key=api_key)
        
        print("Creating OpenAI chat completion...")  # Debug log
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