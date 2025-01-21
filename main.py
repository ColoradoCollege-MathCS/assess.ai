from gpt4all import GPT4All
from datetime import datetime
import os

def save_chat_history(user_input, ai_response):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("chat_history.txt", "a", encoding='utf-8') as f:
        f.write(f"\n[{timestamp}] User: {user_input}\n")
        f.write(f"[{timestamp}] AI: {ai_response}\n")
        f.write("-" * 50 + "\n")

def load_chat_history():
    if os.path.exists("chat_history.txt"):
        with open("chat_history.txt", "r", encoding='utf-8') as f:
            print("\nPrevious Chat History:")
            print("=" * 50)
            print(f.read())
            print("=" * 50)
            print("\nContinuing Chat...")
    else:
        print("\nNo previous chat history found.")

model = GPT4All("Meta-Llama-3-8B-Instruct.Q4_0.gguf", model_path="models")

# Display previous chat history
load_chat_history()

# Start chat session
with model.chat_session():
    print("\nChat with AI (type 'exit' to quit)")
    print("---------------------------------")
    
    while True:
        user_input = input("\nYou: ").strip()
        
        if user_input.lower() == 'exit':
            print("\nGoodbye!")
            break
            
        if user_input:
            try:
                response = model.generate(user_input, max_tokens=1024)
                print("\nAI:", response)
                save_chat_history(user_input, response)
                
            except Exception as e:
                print(f"\nError: {str(e)}")