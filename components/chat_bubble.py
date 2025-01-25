import tkinter as tk

class ChatBubble(tk.Frame):
    def __init__(self, parent, text, is_user=True, **kwargs):
        super().__init__(parent, bg="#D2E9FC", **kwargs)
        
        # Configure grid to allow message expansion
        self.grid_columnconfigure(0 if not is_user else 1, weight=1)
        
        # Calculate dynamic wraplength based on parent width
        parent_width = parent.winfo_width()
        wrap_width = min(int(parent_width * 0.7), 800)  # Max 70% of parent width, up to 800px
        
        # Message container frame
        msg_frame = tk.Frame(
            self,
            bg="#D2E9FC"
        )
        msg_frame.grid(
            row=0,
            column=1 if is_user else 0,
            sticky="e" if is_user else "w",
            padx=(50 if is_user else 10, 10 if is_user else 50)  
        )
        
        self.message = tk.Label(
            msg_frame,
            text=text,
            wraplength=wrap_width,
            justify=tk.LEFT,
            bg="#0A84FF" if is_user else "#E9E9EB",
            fg="white" if is_user else "black",
            font=("SF Pro Text", 12),
            padx=15,
            pady=10,
            anchor="w"  # Left-align text
        )
        self.message.pack(expand=True, fill="both")
        
        # Bind to window resize to update wraplength
        self.bind('<Configure>', self._on_resize)
        

    def _on_resize(self, event):
        # Update wraplength when window is resized
        new_width = min(int(self.winfo_width() * 0.7), 800)
        self.message.configure(wraplength=new_width)