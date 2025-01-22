from gpt4all import GPT4All
from datetime import datetime
import os

class ChatBot:
    def __init__(self):
        self.model = GPT4All("Meta-Llama-3-8B-Instruct.Q4_0.gguf", model_path="models")
        
    def save_chat_history(self, user_input, ai_response):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("chat_history.txt", "a", encoding='utf-8') as f:
            f.write(f"\n[{timestamp}] User: {user_input}\n")
            f.write(f"[{timestamp}] AI: {ai_response}\n")
            f.write("-" * 50 + "\n")

    def load_chat_history(self):
        if os.path.exists("chat_history.txt"):
            with open("chat_history.txt", "r", encoding='utf-8') as f:
                return f.read()
        return "No previous chat history found."

    def get_response(self, user_input):
        if not user_input.strip():
            return "Please enter a message."
            
        try:
            with self.model.chat_session():
                response = self.model.generate(user_input, max_tokens=1024)
                self.save_chat_history(user_input, response)
                return response
        except Exception as e:
            return f"Error: {str(e)}"