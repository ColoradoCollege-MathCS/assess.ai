import tkinter as tk
from tkinter import ttk

class ChatArea:
    """Manages the scrollable chat area of the application"""
    def __init__(self, parent):
        self.canvas = tk.Canvas(
            parent,
            bg="#D2E9FC",
            highlightthickness=0,
            bd=0
        )
        
        self.scrollable_frame = tk.Frame(
            self.canvas,
            bg="#D2E9FC",
            bd=0,
            highlightthickness=0
        )
        
        self.scrollbar = ttk.Scrollbar(
            parent,
            orient="vertical",
            command=self.canvas.yview
        )
        
        self._setup_canvas()
        self._configure_scrolling()
        
    def _setup_canvas(self):
        """Configure canvas and scrollbar"""
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas_frame = self.canvas.create_window(
            (0, 0),
            window=self.scrollable_frame,
            anchor="nw",
            width=self.canvas.winfo_reqwidth()
        )

    def _configure_scrolling(self):
        """Setup scrolling behavior"""
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.canvas.bind(
            "<Configure>",
            lambda e: self.canvas.itemconfig(self.canvas_frame, width=e.width)
        )
        
    def grid_components(self):
        """Position components in the grid"""
        self.canvas.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 5))
        self.scrollbar.grid(row=1, column=1, sticky="ns")
        
    def smooth_scroll_to_bottom(self, steps=10):
        """Smoothly scroll chat area to bottom"""
        current = self.canvas.yview()[1]
        target = 1.0
        if current < target:
            step_size = (target - current) / steps
            def step(count):
                if count < steps:
                    self.canvas.yview_moveto(current + (step_size * count))
                    self.canvas.after(10, lambda: step(count + 1))
                else:
                    self.canvas.yview_moveto(target)
            step(1)