import tkinter as tk

class LLMsPage:
    def __init__(self, root):
        self.root = root
        self.setup_page()
        
    def setup_page(self):
        container = tk.Frame(self.root, bg="#D2E9FC")
        container.grid(row=1, column=1, sticky="nsew")
        
        # Placeholder content
        tk.Label(
            container,
            text="LLMs",
            font=("SF Pro Display", 24, "bold"),
            bg="#D2E9FC"
        ).pack(pady=20)