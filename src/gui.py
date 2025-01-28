import tkinter as tk
import os
from components.navbar import Navbar
from pages.chat_page import ChatPage
from pages.evaluations_page import EvaluationsPage
from pages.llms_page import LLMsPage
from pages.finetune_page import FinetunePage
from pages.projects_page import ProjectsPage
from pages.home_page import HomePage

class AssessAIGUI:
    def __init__(self, root, chat_history, chatbot):
        self.root = root
        self.chat_history = chat_history
        self.chatbot = chatbot
        self.current_page = None
        self.setup_gui()
        
    def setup_gui(self):
        self._configure_root()
        self._configure_grid()
        self._setup_navbar()
        self.show_page("chat")  # Start with chat page
        
    def _configure_root(self):
        self.root.title("Assess.ai")
        self.root.configure(bg="#D2E9FC")
	
	# gets exact location of logo.png
        __location__ = os.path.realpath(os.path.join(os.getcwd(),os.path.dirname(__file__)))
        path = os.path.abspath(__location__)
        path = path + "/assets/logo.png"
        
    def _configure_grid(self):
        # Configure grid weights
        self.root.grid_rowconfigure(1, weight=1)  # Main content area
        self.root.grid_columnconfigure(1, weight=1)  # Main content area
        
    def _setup_navbar(self):
        self.navbar = Navbar(self.root, self.show_page)
        self.navbar.grid(row=1, column=0, sticky="ns")
        
    def _clear_content(self):
        # Remove the existing page
        for widget in self.root.grid_slaves():
            
            if int(widget.grid_info()["column"]) == 1:
                widget.destroy()
                
    def show_page(self, page_name):
        # Show the new page
        self._clear_content()
        
        # Create new page based on selection
        if page_name == "chat":
            self.current_page = ChatPage(self.root, self.chat_history, self.chatbot)
        elif page_name == "evaluations":
            self.current_page = EvaluationsPage(self.root)
        elif page_name == "llms":
            self.current_page = LLMsPage(self.root)
        elif page_name == "finetune":
            self.current_page = FinetunePage(self.root)
        elif page_name == "projects":
            self.current_page = ProjectsPage(self.root)
        elif page_name == "home":
            self.current_page = HomePage(self.root)
