import tkinter as tk
from tkinter import *
<<<<<<< HEAD
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
        image = PhotoImage(file="logo.png")
        image = image.zoom(5)
        image = image.subsample(32)
        panel = Label(self.root,image = image)
        
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
=======
from tkinter import PhotoImage
#from PIL import Image
#import sys
#print(sys.path)
#create main window
root = tk.Tk()

#image for Logo
image = tk.PhotoImage(file = "logo.png")




root.title("Medscribe.ai")
root.configure(bg="SteelBlue1")
root.geometry("800x800")
#create a label/logo for main window
e = tk.Label(root, text = "Welcome to Medscribe.ai, click anywhere to continue", bg="SteelBlue1",
             fg="Black",
             font = ("Times New Roman",30) )
e.pack()









#image label
image_lbl = tk.Label(root, image=image)
image_lbl.pack()





#if click, remove image
def image_click(event):
    image_lbl.destroy()
    #bigbutton.delete()


root.bind("<Button-1>", image_click)






#GUI FOR INPUT TEXT 
#label
inptlbl = tk.Label(root, text="Please input your medical records in the below text box, and click send to summarize!",
                   bg="SteelBlue1",
                   fg="Black",
                   font= ("Times New Roman",20) )
inptlbl.pack(pady=5)
#textbox for user to paste text 
inputtxt = tk.Text(root, height=10, width=60)
inputtxt.pack(pady=10)






#GUI for OUTPUT TEXT
#llabel
outptlbl = tk.Label(root, text="Your Summarized Records Below!",
                   bg="SteelBlue1",
                   fg="Black",
                   font= ("Times New Roman",20) )
outptlbl.pack(pady = 5)
#textbox
outputtxt = tk.Text(root, height=10, width=60)
outputtxt.pack(pady = 10)

#makesure output widget is read only
outputtxt.config(state=DISABLED) #disable editing for display purposes














#creating button

#integrat AI code

def button_clicked():
     #debugging purposes
    print("Clicked Button!")
    inp = inputtxt.get(1.0, "end-1c")
    outputtxt.config(state=NORMAL)#bring back editing
    outputtxt.delete(1.0, END) #clear anuthing from prev
    outputtxt.insert(1.0, "Summarized input: "+inp) #take out summarized input eventually
    outputtxt.config(state=DISABLED) #disable editing agaimn
    
    
   



    #button with specified ops
button = tk.Button(root,text = "Send",command=button_clicked,
                               activebackground="blue",
                               activeforeground="white",
                                anchor="center",
                                 bd=3,
                                bg="purple",
                                cursor="hand2",

                               fg="black",
                               font=("Times New Roman",12),
                               height=6,
                               highlightbackground="black",
                               highlightcolor="green",
                               highlightthickness=2,
                               justify="center",
                               overrelief="raised",
                               padx=10, pady=5, width=15, wraplength=100)
button.pack(pady = 20)



#quit with esc bar
root.bind('<Escape>', lambda e: quit_root(e))
def quit_root(e):
    root.destroy()
#start GUI
root.mainloop()

#implement scroll if text is long - button goes off of page -
# make the textbox output scrolling



#button click- triggers AI process aka ronan



>>>>>>> 7472f7c1939be3034df21d401db5197231e962da
