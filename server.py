from flask import Flask, render_template, jsonify, request, Response, stream_with_context
from flask_cors import CORS
from app.backend_pipeline import generate_answer
from app.systemprompts import SYSTEM_PROMPTS
import time

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/chat', methods=['GET', 'POST'])
def chat():
    try:
        if request.method == 'POST':
            # Get API key from Authorization header
            auth_header = request.headers.get('Authorization')
            if not auth_header or not auth_header.startswith('Bearer '):
                return jsonify({"error": "No API key provided"}), 401
            
            api_key = auth_header.split(' ')[1]  # Extract API key
            print(f"Received API key in server: {api_key[:8]}...")  # Debug log
            
            data = request.json
            message = data.get('message')
            mode = data.get('mode')
            
            # Validate mode
            valid_modes = ['Matte', 'NO', 'Språk', 'SYV']
            if mode not in valid_modes:
                return jsonify({"error": f"Invalid mode. Must be one of: {valid_modes}"}), 400
                
            history = data.get('history', [])
            
            print(f"Received message: {message}, mode: {mode}")  # Debug log
            print(f"History: {history}")  # Debug log
            
            messages = [
                {"role": "user", "content": message}
            ]
            
            def generate():
                try:
                    print("Starting to generate response...")  # Debug log
                    yield "data: \n\n"
                    
                    for token in generate_answer(messages, history=history, mode=mode, api_key=api_key):
                        if token:
                            print(f"Sending token: {token}")  # Debug log
                            yield f"data: {token}\n\n"
                    
                    print("Finished generating response")  # Debug log
                    yield "data: [DONE]\n\n"
                    
                except Exception as e:
                    error_message = str(e)
                    print(f"Error in generate: {error_message}")
                    yield f"data: Error: {error_message}\n\n"
                    
            return Response(stream_with_context(generate()), mimetype='text/event-stream')
            
        return jsonify({"error": "Method not allowed"}), 405
        
    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/test')
def test_stream():
    def generate_test():
        for i in range(5):
            yield f"data: Test message {i}\n\n"
            time.sleep(1)
    
    response = Response(stream_with_context(generate_test()), mimetype='text/event-stream')
    response.headers['Cache-Control'] = 'no-cache'
    response.headers['Connection'] = 'keep-alive'
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

if __name__ == '__main__':
    app.run(debug=True)