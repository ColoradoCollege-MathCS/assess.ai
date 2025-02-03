import tkinter as tk
from tkinter import ttk
import threading
from tkinter import messagebox
from components import (
    ChatBubble, 
    InputFrame, 
    TitleFrame, 
    ChatArea, 
    LoadingIndicator,
    ModelSelector
)
<<<<<<< HEAD
from utils.chat import ChatBot
=======
from utils.chat import ChatBot  
>>>>>>> a0610ba1835c74dcf76d954652a1a43adb5e15a1

class ChatPage:
    def __init__(self, root):
        self.root = root
        self.chatbot = ChatBot()  
        self.is_processing = False
        
        # Create main container for chat page
        self.container = tk.Frame(root, bg="#D2E9FC")
        self.container.grid(row=1, column=1, sticky="nsew")
        
        self.setup_screen()
        
    def setup_screen(self):
        self._configure_root()
        self._setup_styles()
        self._configure_grid()
        self._initialize_components()
<<<<<<< HEAD
        self._initialize_model_selector()
=======
        self._setup_bindings()
        # Load chat history after GUI is ready (100ms delay)
        threading.Thread(target=self.chatbot._load_model, daemon=True).start()
        self.root.after(100, self.load_chat_history)
>>>>>>> a0610ba1835c74dcf76d954652a1a43adb5e15a1
        
    def _configure_root(self):
        self.root.title("Assess.ai")
        self.root.configure(bg="#D2E9FC")
        
    def _setup_styles(self):
        style = ttk.Style()
        style.configure("Chat.TFrame", background="#D2E9FC")
        style.configure("Round.TLabel", background="#D2E9FC")
            
    def _configure_grid(self):
        self.container.grid_rowconfigure(0, weight=0)  # Title
        self.container.grid_rowconfigure(1, weight=0)  # Model Selector
        self.container.grid_rowconfigure(2, weight=1)  # Chat
        self.container.grid_rowconfigure(3, weight=0)  # Input
        self.container.grid_columnconfigure(0, weight=1)
        
    def _initialize_components(self):
        # Title
        self.title_frame = TitleFrame(self.container)
        self.title_frame.grid(row=0, column=0, sticky="ew", pady=(0, 5))

        # Model Selector
        self.model_selector = ModelSelector(self.container, self._on_model_select)
        self.model_selector.grid(row=1, column=0, columnspan=2, sticky="ew")
        
        # Chat area
        self.chat_area = ChatArea(self.container)
        self.chat_area.grid_components()
        self.chat_area.canvas.grid(row=2, column=0, sticky="nsew", padx=20, pady=(0, 5))
        self.chat_area.scrollbar.grid(row=2, column=1, sticky="ns")
        
        # Loading indicator
        self.loading = LoadingIndicator(self.chat_area.scrollable_frame, self.root)
        
        # Input area
        self.input_frame = InputFrame(self.container, self.send_message)
        self.input_frame.grid(row=3, column=0, sticky="ew", padx=20, pady=(0, 10))

    def _initialize_model_selector(self):
        available_models = self.chatbot.get_available_models()
        if not available_models:
            messagebox.showerror("Error", "No models found in model_files directory")
            return
        # Propagate to model selector on what models are available
        self.model_selector.set_models(available_models)
        try:
            # Default to first model
            self._on_model_select(available_models[0])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load initial model: {str(e)}")

    def _on_model_select(self, model_name):
        try:
            # Clear existing chat
            for widget in self.chat_area.scrollable_frame.winfo_children():
                widget.destroy()
            # Load model in background
            threading.Thread(target=self.chatbot.set_model, args=(model_name,), daemon=True).start()
            self.load_chat_history()
                
        except Exception as e:
            messagebox.showerror("Error", str(e))
        
<<<<<<< HEAD
    def set_loading_state(self, is_processing):
        # Loading animation
=======
    def _setup_bindings(self):
        self.root.bind('<Escape>', lambda e: self.root.destroy())
        
    def set_processing_state(self, is_processing):
>>>>>>> a0610ba1835c74dcf76d954652a1a43adb5e15a1
        self.is_processing = is_processing
        self.root.after(0, self._update_input_state)
        
    def _update_input_state(self):
        if hasattr(self.input_frame, 'input_field'):
            self.input_frame.input_field.configure(state='disabled' if self.is_processing else 'normal')
        if hasattr(self.input_frame, 'send_button'):
            self.input_frame.send_button.configure(state='disabled' if self.is_processing else 'normal')
        
    def send_message(self, message):
        if not message.strip() or self.is_processing:  # Check processing state
            return
            
        try:
            # Add user message to chat
            self.add_message(message, is_user=True)
            self.root.update()
            self.loading.start()
            self.set_loading_state(True)  # Disable input while processing
            
            # Start AI response thread
            self._get_ai_response_threaded(message)
            
        except Exception as e:
            print(f"Error sending message: {str(e)}")
<<<<<<< HEAD
            self.set_loading_state(False)  
=======
            self.set_processing_state(False)  # Fixed: was True before
>>>>>>> a0610ba1835c74dcf76d954652a1a43adb5e15a1
        
    def _get_ai_response_threaded(self, user_input):
        def get_response():
            try:
                response = self.chatbot.get_response(user_input)
                self.root.after(0, self._handle_ai_response, response)
            except Exception as e:
                self.root.after(0, self._handle_ai_error, f"Error: {str(e)}")
        
        threading.Thread(target=get_response, daemon=True).start()
            
    def _handle_ai_response(self, response):
        try:
            self.loading.stop()
            self.add_message(response, is_user=False)
            # After adding AI response, ensure we scroll to bottom
            self.root.after(100, self.chat_area.smooth_scroll_to_bottom)
<<<<<<< HEAD
            self.set_loading_state(False)  # Re-enable input after response
=======
            self.set_processing_state(False)  # Re-enable input after response
>>>>>>> a0610ba1835c74dcf76d954652a1a43adb5e15a1
        except Exception as e:
            print(f"Error handling response: {str(e)}")
            
    def _handle_ai_error(self, error_msg):
        self.loading.stop()
        self.add_message(error_msg, is_user=False)
        self.set_loading_state(False)  # Re-enable input on error
        
    def add_message(self, text, is_user=True):
        bubble = ChatBubble(self.chat_area.scrollable_frame, text, is_user=is_user)
        bubble.pack(
            anchor="e" if is_user else "w",  # Right align for user, left for AI
            padx=20,
            pady=5,
            fill="x"
        )
        # Update the scroll region to include new message
        self.chat_area.canvas.update_idletasks()
        self.chat_area.canvas.configure(scrollregion=self.chat_area.canvas.bbox("all"))
        
        self.chat_area.smooth_scroll_to_bottom()
            
    def load_chat_history(self):
        try:
            entries = self.chatbot.load_chat_history()  
            for entry in entries:
                chat_data = entry['data']
                self.add_message(chat_data['user_input'], is_user=True)
                self.add_message(chat_data['ai_response'], is_user=False)
        except Exception as e:
            print(f"Error loading chat history: {str(e)}")
        
        self.root.after(50, lambda: self.chat_area.canvas.yview_moveto(5.0))


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