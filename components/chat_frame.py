import tkinter as tk
from tkinter import ttk
from components.chat_bubble import ChatBubble

class ChatFrame(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg="#87CEEB", **kwargs)
        
        # Create canvas for scrolling without border
        self.canvas = tk.Canvas(
            self,
            bg="#87CEEB",
            bd=0,
            highlightthickness=0,
            relief='flat'
        )
        self.scrollable_frame = tk.Frame(
            self.canvas,
            bg="#87CEEB",
            bd=0
        )
        
        # Custom style for scrollbar
        style = ttk.Style()
        style.configure("Custom.Vertical.TScrollbar",
                       background="#87CEEB",
                       bordercolor="#87CEEB",
                       arrowcolor="#87CEEB",
                       troughcolor="#87CEEB")
        
        # Add scrollbar with custom style
        self.scrollbar = ttk.Scrollbar(
            self,
            orient="vertical",
            command=self.canvas.yview,
            style="Custom.Vertical.TScrollbar"
        )
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Layout
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        
        # Create window for scrollable frame
        self.canvas_frame = self.canvas.create_window(
            (0, 0),
            window=self.scrollable_frame,
            anchor="nw",
            width=self.canvas.winfo_reqwidth()
        )
        
        # Configure bindings
        self.scrollable_frame.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind("<Configure>", self.on_canvas_configure)
        
        # Bind mouse wheel
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def on_frame_configure(self, event=None):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_canvas_configure(self, event):
        # Update the width of the window inside the canvas
        self.canvas.itemconfig(self.canvas_frame, width=event.width)

    def add_message(self, text, is_user=True):
        bubble = ChatBubble(self.scrollable_frame, text, is_user=is_user)
        bubble.pack(
            anchor="e" if is_user else "w",
            padx=20,
            pady=5
        )
        # Scroll to bottom
        self.canvas.update_idletasks()
        self.canvas.yview_moveto(1)