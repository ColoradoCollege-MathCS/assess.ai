import tkinter as tk
from tkinter import ttk
import threading
from components import (ChatBubble, InputFrame, TitleFrame, 
                       ChatArea, LoadingIndicator, LoginScreen)

class MedscribeGUI:
    def __init__(self, root, chat_history, chatbot):
        self.root = root  # Main Window
        self.chat_history = chat_history  # Variable managing message history
        self.chatbot = chatbot  # Handles LLM Responses
        self.is_processing = False  # State tracking for message processing
        self.setup_login_screen()  # Start login screen
        
    def setup_login_screen(self):
        """Initialize login screen"""
        self._clear_window()
        self.login_screen = LoginScreen(
            self.root,
            on_login_success=self.setup_chat_screen,
            chat_history=self.chat_history  # Pass chat_history here
        )
        self.login_screen.grid(row=0, column=0, sticky="nsew")
        
    def _clear_window(self):
        """Clear all widgets from window"""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    # Layout for overall app
    def _configure_root(self, title, geometry="1000x1200"):
        self.root.title(title)
        self.root.configure(bg="#D2E9FC")
        self.root.geometry(geometry)
            
    def _setup_styles(self):
        style = ttk.Style()
        style.configure("Chat.TFrame", background="#D2E9FC")
        style.configure("Round.TLabel", background="#D2E9FC")
            
    def setup_chat_screen(self):
        """Setup main chat interface"""
        self._clear_window()
        self._configure_root("Medscribe.ai", "1000x1200")
        self._setup_styles()
        self._configure_grid()
        self._initialize_components()
        self._setup_bindings()
        # Load chat history after GUI is ready (100ms delay)
        self.root.after(100, self.load_chat_history)

    def _configure_grid(self):
        self.root.grid_rowconfigure(0, weight=0)  # Title
        self.root.grid_rowconfigure(1, weight=1)  # Chat
        self.root.grid_rowconfigure(2, weight=0)  # Input
        self.root.grid_columnconfigure(0, weight=1)
        
    def _initialize_components(self):
        # Title
        self.title_frame = TitleFrame(self.root)
        self.title_frame.grid(row=0, column=0, sticky="ew", pady=(0, 5))
        
        # Chat area
        self.chat_area = ChatArea(self.root)
        self.chat_area.grid_components()
        
        # Loading indicator
        self.loading = LoadingIndicator(self.chat_area.scrollable_frame, self.root)
        
        # Input area
        self.input_frame = InputFrame(self.root, self.send_message)
        self.input_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=(0, 10))
        
    def _setup_bindings(self):
        self.root.bind('<Escape>', lambda e: self.root.destroy())
        
    def set_processing_state(self, is_processing):
        """Update processing state and input frame state"""
        self.is_processing = is_processing
        self.root.after(0, self._update_input_state)
        
    def _update_input_state(self):
        """Update input frame enabled/disabled state"""
        if hasattr(self.input_frame, 'input_field'):
            self.input_frame.input_field.configure(state='disabled' if self.is_processing else 'normal')
        if hasattr(self.input_frame, 'send_button'):
            self.input_frame.send_button.configure(state='disabled' if self.is_processing else 'normal')
        
    def send_message(self, message):
        if not message.strip() or self.is_processing:  # Check processing state
            return
            
        try:
            # Add user message to chat
            current_scroll = self.chat_area.canvas.yview()[0]
            self.add_message(message, is_user=True)
            self.root.update()
            self.loading.start()
            self.set_processing_state(True)  # Disable input while processing
            
            # Start AI response thread
            self._get_ai_response_threaded(message, current_scroll)
            
        except Exception as e:
            print(f"Error sending message: {str(e)}")
            self.add_message(f"Error: {str(e)}", is_user=False)
            self.set_processing_state(False)
        
    def _get_ai_response_threaded(self, user_input, scroll_position):
        def get_response():
            try:
                response = self.chatbot.get_response(user_input)
                self.root.after(0, self._handle_ai_response, response, user_input, scroll_position)
            except Exception as e:
                self.root.after(0, self._handle_ai_error, f"Error: {str(e)}")
        
        thread = threading.Thread(target=get_response)
        thread.daemon = True
        thread.start()
            
    def _handle_ai_response(self, response, user_input, scroll_position):
        try:
            self.loading.stop()
            self.add_message(response, is_user=False)
            # After adding AI response, ensure we scroll to bottom
            self.root.after(100, self.chat_area.smooth_scroll_to_bottom)
            self.chat_history.save_chat_entry({
                'user_input': user_input,
                'ai_response': response
            })
            self.set_processing_state(False)  # Re-enable input after response
        except Exception as e:
            print(f"Error handling response: {str(e)}")
            
    def _handle_ai_error(self, error_msg):
        self.loading.stop()
        self.add_message(error_msg, is_user=False)
        self.set_processing_state(False)  # Re-enable input on error
        
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
            entries = self.chat_history.load_chat_history()
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