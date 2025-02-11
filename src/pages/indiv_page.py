import sys
import tkinter as tk
import io
from tkinter import ttk
from components.llm_details import LLMDetails


class LLMPage:
    def __init__(self, root, llm):
        self.LLM = llm
        self.root = root
        self.container = tk.Frame(self.root, bg="#D2E9FC")
        self.container.grid(row=1, column=1, sticky="nsew")

        self.setup_page()

    def setup_page(self):
        """Initialize and set up the LLM Individual page """
        self._configure_root()
        self._configure_grid()
        self._setup_styles()
        self._initialize_components()
        self._setup_bindings()

    def _configure_root(self):
        """Configure root window settings"""
        self.root.title("Assess.ai")
        self.root.configure(bg="#D2E9FC")

    def _configure_grid(self):
        """Configure grid layout"""
        self.container.grid_rowconfigure(0, weight=1)  # LLM Name + Details
        self.container.grid_columnconfigure(0, weight=1)

    def _setup_styles(self):
        """Setup ttk styles"""
        style = ttk.Style()

    def _setup_bindings(self):
        self.root.bind('<Escape>', lambda e: self.root.destroy())

    def _initialize_components(self):

        # Name + Details
        self.details_frame = LLMDetails(self.container, self.LLM)
        self.details_frame.grid(row=0, column=0, sticky="ew", pady=(0,50))
