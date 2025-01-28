import tkinter as tk
from PIL import Image, ImageTk
from pathlib import Path

# Navigation items
nav_items = [
    ("Home","home"),
    ("Chat", "chat"),
    ("Evaluations", "evaluations"),
    ("LLMs", "llms"),
    ("Finetune", "finetune"),
    ("Projects", "projects")
]

class Navbar(tk.Frame):
    def __init__(self, parent, show_page_callback, **kwargs):
        super().__init__(parent, bg="#FFFFFF", **kwargs)
        self.show_page_callback = show_page_callback
        self.current_page = "chat"  # Default page
        self.buttons = {}  # Store button references
        self._setup_navbar()
        
    def _setup_navbar(self):
        self.grid_columnconfigure(0, weight=1)
        
        nav_container = tk.Frame(
            self, 
            bg="#FFFFFF",
            width=250,
            highlightbackground="#E5E5E5",
            highlightthickness=1
        )
        nav_container.pack(side="left", fill="y", pady=0)
        
        logo_container = tk.Frame(nav_container, bg="#FFFFFF", height=100)
        # Fills horizontal space
        logo_container.pack(fill="x", pady=(20, 30))
        
        try:
            logo_img = Image.open(Path("assets/logo.jpeg"))
            logo_width = 180  
            aspect_ratio = logo_img.height / logo_img.width
            logo_height = int(logo_width * aspect_ratio)
            logo_img = logo_img.resize((logo_width, logo_height), Image.Resampling.LANCZOS)
            logo_photo = ImageTk.PhotoImage(logo_img)
            
            logo_label = tk.Label(
                logo_container,
                image=logo_photo,
                bg="#FFFFFF"
            ) 
            logo_label.pack(pady=(0, 20))
            
        except Exception as e:
            print(f"Error loading logo: {str(e)}")
            # Fallback text if image fails to load
            tk.Label(
                logo_container,
                text="Assess.ai",
                font=("SF Pro Display", 24, "bold"),
                bg="#FFFFFF",
                fg="#1a1a1a"
            ).pack(pady=20)

        
        buttons_container = tk.Frame(nav_container, bg="#FFFFFF")
        buttons_container.pack(fill="x", padx=20)
        
        for text, page in nav_items:
            btn_container = tk.Frame(buttons_container, bg="#FFFFFF")
            btn_container.pack(fill="x", pady=5)
            
            btn = tk.Label(
                btn_container,
                text=text,
                font=("SF Pro Text", 14),
                bg="#FFFFFF",
                fg="#1a1a1a",
                cursor="hand1",
                padx=15,
                pady=10,
                anchor="w"  # Left-align text
            )
            btn.pack(fill="x", ipady=5)
            
            self.buttons[page] = {
                'button': btn,
                'container': btn_container
            }
            
            btn.bind("<Button-1>", lambda e, p=page: self._handle_click(p))
            btn.bind("<Enter>", lambda e, b=btn_container, p=page: self._on_hover(b, p))
            btn.bind("<Leave>", lambda e, b=btn_container, p=page: self._on_leave(b, p))
        
        self.set_active_page("chat")

    def _handle_click(self, page):
        if page != self.current_page:
            self.show_page_callback(page)
            self.set_active_page(page)

    def set_active_page(self, page):
        self.current_page = page
        
        for p, elements in self.buttons.items():
            if p == page:
                # Button style for active page
                elements['container'].configure(bg="#E8F0FE")
                elements['button'].configure(
                    bg="#E8F0FE",
                    fg="#1A73E8",
                    cursor="arrow"
                )
            else:
                # Button style for inactive page
                elements['container'].configure(bg="#FFFFFF")
                elements['button'].configure(
                    bg="#FFFFFF",
                    fg="#1a1a1a",
                    cursor="hand2"
                )
# Hover effect
    def _on_hover(self, container, page):
        if page != self.current_page:
            container.configure(bg="#F8F9FA")
            for child in container.winfo_children():
                child.configure(bg="#F8F9FA")

    def _on_leave(self, container, page):
        if page != self.current_page:
            container.configure(bg="#FFFFFF")
            for child in container.winfo_children():
                child.configure(bg="#FFFFFF")
        else:
            container.configure(bg="#E8F0FE")
            for child in container.winfo_children():
                child.configure(bg="#E8F0FE")