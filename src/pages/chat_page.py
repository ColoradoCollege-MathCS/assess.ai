import tkinter as tk
from tkinter import ttk
import threading
from components import (
    ChatBubble, 
    InputFrame, 
    TitleFrame, 
    ChatArea, 
    LoadingIndicator
)

class ChatPage:
    def __init__(self, root, chat_history, chatbot):
        self.root = root
        self.chat_history = chat_history
        self.chatbot = chatbot
        self.is_processing = False
        
        # Create main container for chat page
        self.container = tk.Frame(root, bg="#D2E9FC")
        self.container.grid(row=1, column=1, sticky="nsew")
        
        self.setup_screen()
        
    def setup_screen(self):
        """Initialize and setup the chat screen"""
        self._configure_root()
        self._setup_styles()
        self._configure_grid()
        self._initialize_components()
        self._setup_bindings()
        # Load chat history after GUI is ready (100ms delay)
        self.root.after(100, self.load_chat_history)
        
    def _configure_root(self):
        """Configure root window settings"""
        self.root.title("Assess.ai")
        self.root.configure(bg="#D2E9FC")
        
    def _setup_styles(self):
        """Setup ttk styles"""
        style = ttk.Style()
        style.configure("Chat.TFrame", background="#D2E9FC")
        style.configure("Round.TLabel", background="#D2E9FC")
            
    def _configure_grid(self):
        """Configure grid layout"""
        self.container.grid_rowconfigure(0, weight=0)  # Title
        self.container.grid_rowconfigure(1, weight=1)  # Chat
        self.container.grid_rowconfigure(2, weight=0)  # Input
        self.container.grid_columnconfigure(0, weight=1)
        
    def _initialize_components(self):
        # Title
        self.title_frame = TitleFrame(self.container)
        self.title_frame.grid(row=0, column=0, sticky="ew", pady=(0, 5))
        
        # Chat area
        self.chat_area = ChatArea(self.container)
        self.chat_area.grid_components()
        
        # Loading indicator
        self.loading = LoadingIndicator(self.chat_area.scrollable_frame, self.root)
        
        # Input area
        self.input_frame = InputFrame(self.container, self.send_message)
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