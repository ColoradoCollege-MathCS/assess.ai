import tkinter as tk
import threading
from gui import AssessAIGUI
from chat_history import SecureChatHistory
from chat import ChatBot
import os
os.environ['TOKENIZERS_PARALLELISM'] = 'false'

def main():
    # Initialize root and components
    root = tk.Tk()
    root.title("AssessAI")
    root.geometry("1000x1200")
    
    # Configure grid weights for the root window
    root.grid_rowconfigure(1, weight=1)  # Make row 1 expandable
    root.grid_columnconfigure(1, weight=1)  # Make column 1 expandable
    
    # Load chat history
    chat_history = SecureChatHistory()
    
    # Create chatbot without loading model
    chatbot = ChatBot()
    
    # Create GUI
    app = AssessAIGUI(root, chat_history, chatbot)
    
    # Start model loading in background
    def load_model_background():
        chatbot._load_model()
        print("Model loaded and ready!")
    
    threading.Thread(target=load_model_background, daemon=True).start()
    
    # Start main loop
    root.mainloop()

if __name__ == "__main__":
    main()

"""
We use threading in this app to keep app responsive while the LLM response is being returned. 
Before without threading, the app would pause and not be responsive until the LLM response comes. 
By using threading we allow the UI to work while doing other tasks. 

2 threads: Main Thread (UI), AI Response threads (Created when needing to get response).

# THREAD FLOW DIAGRAM
#
# Main UI Thread                    AI Response Thread
# (tkinter)                        (spawned as needed)
# ================                 ==================
#      |                                  |
#      |                                  |
# User types...                          |
#      |                                  |
# [Send clicked]                         |
#      |                                  |
# send_message()                         |
#   |                                    |
#   |---> Add user message              |
#   |     to chat                       |
#   |                                    |
#   |---> Start AI Thread ------------->|
#      |                                  |
#      |                         [Process AI response]
# [UI remains                            |
#  responsive]                   [AI response ready]
#      |                                  |
#      |<---------------------------------|
#      |                    root.after()  |
# [Show AI reply]           (schedule UI  |
#      |                    update)       |
#      |                                  |
#
# Notes:
# - Main UI Thread: Never blocks, handles all UI updates
# - AI Thread: Created for each response, dies after completion
# 
# Key Points:
# 1. UI never freezes because heavy processing is offloaded
# 2. Direct message handling without queues
# 3. root.after() safely schedules UI updates from other threads
# 4. Due to GIL, only one Python thread runs at a time
#    (but switches fast enough to appear concurrent)
"""