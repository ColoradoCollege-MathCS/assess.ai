import tkinter as tk
import os
from components.navbar import Navbar
from pages.evaluation_page import EvaluationPage
from pages.llms_page import LLMsPage
from pages.finetune_page import FinetunePage
from pages.home_page import HomePage


# Set environment variable
os.environ['TOKENIZERS_PARALLELISM'] = 'false'

class AssessAIGUI:
    def __init__(self, root):
        self.root = root
        self.current_page = None
        self.setup_gui()
        # Calls function below
        
    def setup_gui(self):
        self._configure_root()
        self._configure_grid()
        self._setup_navbar()
        
    def _configure_root(self):
        self.root.title("Assess.ai")
        self.root.configure(bg="#D2E9FC")
        
    def _configure_grid(self):
        # Configure grid weights
        self.root.grid_rowconfigure(1, weight=1)  # Main content area
        self.root.grid_columnconfigure(1, weight=1)  # Main content area
        
    def _setup_navbar(self):
        # Set callback function for changing the page 
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

        if page_name == "evaluations":
            self.current_page = EvaluationPage(self.root)
        elif page_name == "llms":
            self.current_page = LLMsPage(self.root)
        elif page_name == "finetune":
            self.current_page = FinetunePage(self.root)
        elif page_name == "home":
            self.current_page = HomePage(self.root, self.show_page)


def main():
    # Initialize root and components
    root = tk.Tk()
    root.title("AssessAI")
    root.geometry("1000x1200")
    
    # Configure grid weights for the root window
    root.grid_rowconfigure(1, weight=1)  # Make row 1 expandable
    root.grid_columnconfigure(1, weight=1)  # Make column 1 expandable

    # Initialize GUI
    app = AssessAIGUI(root)
    app.show_page("home")
    
    # Start main loop
    root.mainloop()

if __name__ == "__main__":
    main()
