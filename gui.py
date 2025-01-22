import tkinter as tk
from tkinter import scrolledtext
from chat import ChatBot

class MedscribeGUI:
    def __init__(self, root):
        self.root = root
        self.chatbot = ChatBot()
        self.setup_gui()
        
    def setup_gui(self):
        self.root.title("Medscribe.ai")
        self.root.configure(bg="SteelBlue1")
        self.root.geometry("800x800")

        # Title
        title = tk.Label(
            self.root,
            text="Welcome to Medscribe.ai",
            bg="SteelBlue1",
            fg="Black",
            font=("Times New Roman", 50)
        )
        title.pack(pady=10)

        # Chat history display
        self.chat_display = scrolledtext.ScrolledText(
            self.root,
            height=20,
            width=60,
            font=("Times New Roman", 12)
        )
        self.chat_display.pack(pady=10)
        
        # Load chat history
        self.chat_display.insert(tk.END, self.chatbot.load_chat_history())

        # Input textbox
        self.input_text = scrolledtext.ScrolledText(
            self.root,
            height=10,
            width=60,
            font=("Times New Roman", 12)
        )
        self.input_text.pack(pady=10)

        # Send button
        self.send_button = tk.Button(
            self.root,
            text="Send",
            command=self.send_message,
            activebackground="blue",
            activeforeground="white",
            bg="purple",
            fg="black",
            font=("Times New Roman", 12),
            height=2,
            width=15
        )
        self.send_button.pack(pady=10)

        # Bind escape key to quit
        self.root.bind('<Escape>', lambda e: self.root.destroy())

    def send_message(self):
        user_input = self.input_text.get("1.0", tk.END).strip()
        if user_input:
            # Display user message
            self.chat_display.insert(tk.END, f"\nYou: {user_input}\n")
            self.chat_display.see(tk.END)
            
            # Get and display AI response
            response = self.chatbot.get_response(user_input)
            self.chat_display.insert(tk.END, f"AI: {response}\n")
            self.chat_display.insert(tk.END, "-" * 50 + "\n")
            self.chat_display.see(tk.END)
            
            # Clear input
            self.input_text.delete("1.0", tk.END)