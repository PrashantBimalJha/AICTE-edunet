from flask import Flask, request, jsonify

app = Flask(__name__)

# Predefined questions and answers (adding simple greetings)
qa_pairs = {
    "hi": "Hello! How can I assist you today?",
    "hello": "Hi there! How can I help you?",
    "how are you": "I am just code, but I'm functioning perfectly!",
    "what is your name": "I am ChatBot!",
    "what is python": "Python is a high-level programming language.",
    "what is flask": "Flask is a lightweight Python web framework.",
    "tell me a joke": "Why did the programmer go broke? Because he used up all his cache!",
    "what is ai": "AI stands for Artificial Intelligence.",
    "what is html": "HTML stands for HyperText Markup Language.",
    "what is css": "CSS stands for Cascading Style Sheets.",
    "what is javascript": "JavaScript is a programming language for the web.",
    "bye": "Goodbye! Have a nice day!",
}

@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>ChatBot</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            body {
                font-family: 'Arial', sans-serif;
                background-color: #181818;
                color: #e0e0e0;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                padding: 0 10px;
            }
            .chat-container {
                width: 100%;
                max-width: 700px;
                background: #1e1e1e;
                border-radius: 12px;
                box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3);
                padding: 30px;
                display: flex;
                flex-direction: column;
                height: 80vh;
                animation: fadeIn 1s ease-in-out;
            }
            .chat-box {
                flex: 1;
                overflow-y: auto;
                margin-bottom: 20px;
                padding: 20px;
                background-color: #333;
                border-radius: 8px;
                border: 1px solid #444;
                max-height: 100%;
                animation: expand 0.8s ease-in-out;
                margin-bottom: 30px;
            }
            .message {
                margin-bottom: 15px;
                max-width: 80%;
                padding: 12px;
                border-radius: 10px;
                animation: fadeInMessage 0.8s ease-in-out;
            }
            .user {
                text-align: right;
                color: #4CAF50;
                background-color: #333;
                border: 1px solid #444;
            }
            .bot {
                text-align: left;
                color: #fff;
                background-color: #444;
                border: 1px solid #555;
            }
            .input-container {
                display: flex;
            }
            input[type="text"] {
                flex: 1;
                padding: 15px;
                border: 1px solid #555;
                border-radius: 8px;
                font-size: 16px;
                color: #fff;
                background-color: #444;
                margin-right: 10px;
                transition: all 0.3s ease;
            }
            input[type="text"]:focus {
                outline: none;
                border-color: #4CAF50;
                background-color: #555;
            }
            button {
                padding: 12px 20px;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 8px;
                cursor: pointer;
                font-size: 16px;
                transition: background-color 0.3s ease;
            }
            button:hover {
                background-color: #45a049;
            }
            /* Animation effects */
            @keyframes fadeIn {
                from { opacity: 0; }
                to { opacity: 1; }
            }
            @keyframes fadeInMessage {
                from { opacity: 0; transform: translateY(20px); }
                to { opacity: 1; transform: translateY(0); }
            }
            @keyframes expand {
                from { max-height: 100px; }
                to { max-height: 100%; }
            }
        </style>
    </head>
    <body>
        <div class="chat-container">
            <div class="chat-box" id="chat-box"></div>
            <div class="input-container">
                <input type="text" id="user-input" placeholder="Ask me anything..." onkeydown="if(event.key === 'Enter'){sendMessage();}">
                <button onclick="sendMessage()">Send</button>
            </div>
        </div>
        <script>
            function sendMessage() {
                const userInput = document.getElementById('user-input');
                const chatBox = document.getElementById('chat-box');
                const userMessage = userInput.value.trim().toLowerCase(); // Convert to lowercase

                if (!userMessage) return;

                // Display user message with animation
                chatBox.innerHTML += `<div class="message user">${userMessage}</div>`;
                userInput.value = '';

                // Send request to backend for response
                fetch('/get_answer', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ question: userMessage })
                })
                .then(response => response.json())
                .then(data => {
                    // Display bot response with animation
                    chatBox.innerHTML += `<div class="message bot">${data.answer}</div>`;
                    chatBox.scrollTop = chatBox.scrollHeight;
                })
                .catch(err => {
                    chatBox.innerHTML += `<div class="message bot">Error: Unable to fetch the response.</div>`;
                });
            }
        </script>
    </body>
    </html>
    '''

@app.route('/get_answer', methods=['POST'])
def get_answer():
    user_question = request.json.get('question', '').strip().lower()  # Normalize the question to lowercase
    answer = qa_pairs.get(user_question, "I don't understand that question.")
    return jsonify({"answer": answer})

if __name__ == '__main__':
    # Run the Flask app locally
    app.run(debug=True, host='0.0.0.0', port=5000)
