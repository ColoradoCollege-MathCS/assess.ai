import tkinter as tk
import threading
from gui import MedscribeGUI
from chat_history import SecureChatHistory
from chat import ChatBot
import os
os.environ['TOKENIZERS_PARALLELISM'] = 'false'

def main():
    # Initialize root and components
    root = tk.Tk()
    root.geometry("1000x1200")
    
    # Load chat history
    chat_history = SecureChatHistory()
    
    # Create chatbot without loading model
    chatbot = ChatBot()
    
    # Create GUI
    app = MedscribeGUI(root, chat_history, chatbot)
    
    # Start model loading in background. Using threading here allows the GUI to render first when ready and not have to wait until model is ready.
    def load_model_background():
        chatbot._load_model()
        print("Model loaded and ready!")
    
    threading.Thread(target=load_model_background, daemon=True).start()
    
    # Start main loop
    root.mainloop()

if __name__ == "__main__":
    main()