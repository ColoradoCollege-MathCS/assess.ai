import tkinter as tk
from tkinter import ttk
from components.rounded_frame import RoundedFrame
from PIL import Image, ImageTk

class LoginScreen(tk.Frame):
    def __init__(self, parent, on_login_success, chat_history, **kwargs):
        super().__init__(parent, bg="#D2E9FC", **kwargs)
        self.chat_history = chat_history
        self.on_login_success = on_login_success
        self.attempts_remaining = 5
        
        # Configure the frame to fill the parent window
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)
        self.grid(row=0, column=0, sticky="nsew")
        
        self.setup_login_screen()
        
    def setup_login_screen(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=2)  
        self.grid_rowconfigure(1, weight=3)  
        self.grid_rowconfigure(2, weight=2)  
        
        # Logo/Title Section
        img_size = (100, 100)  
        try:
            img = Image.open("assets/logo.png")
            img = img.resize(img_size, Image.Resampling.LANCZOS)
            self.logo_img = ImageTk.PhotoImage(img)
            logo_label = tk.Label(self, image=self.logo_img, bg="#D2E9FC")
        except Exception as e:
            print(f"Error loading logo: {e}")
            logo_label = tk.Label(
                self,
                text="Medscribe.ai",
                bg="#D2E9FC",
                fg="#1a1a1a",
                font=("SF Pro Display", 32, "bold")
            )
        logo_label.grid(row=0, column=0, pady=(20, 10))
        
        # Main Login Container
        login_container = RoundedFrame(self, "#FFFFFF", radius=50)
        login_container.grid(
            row=1, 
            column=0, 
            sticky="n",
            padx=max(100, int(self.winfo_width() * 0.2)),
            pady=(0, 20)
        )
        
        content_frame = tk.Frame(login_container, bg="white")
        content_frame.pack(expand=True, fill="both", padx=30, pady=30)
        
        # Password Label
        password_label = tk.Label(
            content_frame,
            text="Enter Password",
            font=("SF Pro Display", 14, "bold"),
            bg="white",
            fg="#1a1a1a"
        )
        password_label.pack(pady=(0, 15))
        
        # Custom Password Entry Frame
        entry_frame = tk.Frame(content_frame, bg="white")
        entry_frame.pack(pady=(0, 15))
        
        # Create a canvas for the input background
        self.entry_bg = tk.Canvas(
            entry_frame,
            height=40,
            width=280,
            bg="white",
            highlightthickness=0
        )
        self.entry_bg.pack(fill="x")
        
        # Draw rounded rectangle background
        self.draw_entry_background("#F5F5F5")  # Light gray background
        
        # Password Entry
        self.password_entry = tk.Entry(
            entry_frame,
            show="•",
            font=("SF Pro Text", 13),
            bd=0,
            bg="#F5F5F5",
            highlightthickness=0,
            justify="center",
            width=30
        )
        # Position the entry widget over the canvas
        self.entry_bg.create_window(
            140, 20,  # Center position
            window=self.password_entry,
            width=260,
            height=30
        )
        
        # Bind events for visual feedback
        self.password_entry.bind("<FocusIn>", self.on_entry_focus)
        self.password_entry.bind("<FocusOut>", self.on_entry_unfocus)
        
        # Error Message Label
        self.error_label = tk.Label(
            content_frame,
            text="",
            font=("SF Pro Text", 12),
            bg="white",
            fg="#FF3B30",
            wraplength=250
        )
        self.error_label.pack(pady=(0, 15))
        
        # Login Button
        self.login_button = tk.Label(
            content_frame,
            text="Login",
            font=("SF Pro Text", 13, "bold"),
            bg="#4287f5",
            fg="white",
            cursor="hand2"
        )
        self.login_button.pack(pady=(0, 10), ipadx=30, ipady=8)
        
        # Bind events
        self.login_button.bind("<Button-1>", lambda e: self.handle_login())
        self.login_button.bind("<Enter>", lambda e: self.login_button.configure(bg="#3B78DE"))
        self.login_button.bind("<Leave>", lambda e: self.login_button.configure(bg="#4287f5"))
        self.password_entry.bind('<Return>', lambda e: self.handle_login())
        
        # Focus password entry
        self.password_entry.focus()

    def draw_entry_background(self, color, border_color=None):
        """Draw the rounded rectangle background for the entry"""
        width = 280
        height = 40
        radius = 10
        
        if border_color:
            # Draw border
            self.entry_bg.delete("border")
            self.entry_bg.create_rounded_rect(
                2, 2, width-2, height-2, radius,
                fill=color,
                outline=border_color,
                width=2,
                tags="border"
            )
        else:
            # Draw background
            self.entry_bg.delete("bg")
            self.entry_bg.create_rounded_rect(
                0, 0, width, height, radius,
                fill=color,
                tags="bg"
            )

    def on_entry_focus(self, event):
        """Handle entry focus event"""
        self.draw_entry_background("#FFFFFF", "#4287f5")  # White bg with blue border
        self.password_entry.configure(bg="white")

    def on_entry_unfocus(self, event):
        """Handle entry unfocus event"""
        self.draw_entry_background("#F5F5F5")  # Return to light gray
        self.password_entry.configure(bg="#F5F5F5")
    
    def handle_login(self):
        try:
            password = self.password_entry.get()
            self.password_entry.delete(0, 'end')
            
            # Initialize encryption with password
            self.chat_history.initialize_encryption(password)
            
            # If successful, switch to chat screen
            self.on_login_success()
            
        except Exception as e:
            error_msg = str(e)
            if "Maximum password attempts" in error_msg:
                self.error_label.config(text="Maximum attempts exceeded. Please try again later.")
                self.login_button.configure(state="disabled", bg="#D1D1D6")
            elif "Incorrect password" in error_msg:
                self.attempts_remaining -= 1
                self.error_label.config(
                    text=f"Incorrect password. {self.attempts_remaining} attempts remaining."
                )
                if self.attempts_remaining <= 0:
                    self.login_button.configure(state="disabled", bg="#D1D1D6")
            else:
                self.error_label.config(text=error_msg)

# Add rounded rectangle creation method to Canvas class
def create_rounded_rect(self, x1, y1, x2, y2, radius, **kwargs):
    points = [
        x1 + radius, y1,
        x2 - radius, y1,
        x2, y1,
        x2, y1 + radius,
        x2, y2 - radius,
        x2, y2,
        x2 - radius, y2,
        x1 + radius, y2,
        x1, y2,
        x1, y2 - radius,
        x1, y1 + radius,
        x1, y1
    ]
    return self.create_polygon(points, smooth=True, **kwargs)

# Add method to Canvas class
tk.Canvas.create_rounded_rect = create_rounded_rect