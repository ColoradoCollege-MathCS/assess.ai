import tkinter as tk
from components.rounded_frame import RoundedFrame

class InputFrame(tk.Frame):
    def __init__(self, parent, send_callback, **kwargs):
        super().__init__(parent, bg="#D2E9FC", **kwargs)
        self.send_callback = send_callback
        self.setup_input_area()

    def setup_input_area(self):
        self.grid_columnconfigure(0, weight=1)
        
        # Container frame for input and button
        self.container = tk.Frame(self, bg="#D2E9FC")
        self.container.grid(row=0, column=0, sticky="ew", padx=20, pady=15)
        self.container.grid_columnconfigure(0, weight=1)
        
        # Input container with rounded corners
        self.input_container = RoundedFrame(self.container, "#FFFFFF", radius=50)
        self.input_container.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        
        # Text input area
        self.input_text = tk.Text(
            self.input_container,
            height=2,
            font=("SF Pro Text", 13),
            wrap=tk.WORD,
            bd=0,
            bg="white",
            highlightthickness=0,
            relief="flat"
        )
        self.input_text.pack(fill="both", expand=True, padx=15, pady=8)
        
        # Circular send button
        button_size = 40  # Diameter of the circle
        self.send_button = tk.Canvas(
            self.container,
            width=button_size,
            height=button_size,
            bg="#D2E9FC",
            highlightthickness=0,
            cursor="hand2"
        )
        self.send_button.grid(row=0, column=1)
        
        # Draw circular button
        padding = 2  # Space between circle edge and canvas
        self.circle = self.send_button.create_oval(
            padding, padding,
            button_size - padding, button_size - padding,
            fill="#0A84FF",
            outline=""
        )
        
        # Add arrow symbol
        arrow_size = 15
        self.arrow = self.send_button.create_text(
            button_size // 2,  # Center X
            button_size // 2,  # Center Y
            text="↑",
            fill="white",
            font=("SF Pro Text", 20),
            anchor="center"
        )
        
        # Bind events
        self.send_button.bind("<Button-1>", self.handle_send)
        self.send_button.bind("<Enter>", self.on_hover)
        self.send_button.bind("<Leave>", self.on_leave)
        self.input_text.bind("<Return>", self.handle_return)

    def on_hover(self, event):
        self.send_button.itemconfig(self.circle, fill="#0070E0")  # Darker blue on hover

    def on_leave(self, event):
        self.send_button.itemconfig(self.circle, fill="#0A84FF")  # Original blue

    def handle_return(self, event):
        if not event.state & 0x1:  # Shift not pressed
            self.handle_send(None)
            return "break"
        return None

    def handle_send(self, event=None):
        message = self.get_input()
        if message.strip():  # Only send if there's actual text
            self.clear_input()  # Clear input immediately
            self.send_callback(message)  # Pass the message to callback

    def get_input(self):
        return self.input_text.get("1.0", "end-1c").strip()

    def clear_input(self):
        self.input_text.delete("1.0", "end")
        self.input_text.focus()