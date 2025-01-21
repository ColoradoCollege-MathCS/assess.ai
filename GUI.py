import tkinter as tk
from tkinter import *

#create main window
root = tk.Tk()
root.title("Medscribe.ai")
root.configure(bg="SteelBlue1")
root.geometry("800x800")
#create a label
e = tk.Label(root, text = "Welcome to Medscribe.ai", bg="SteelBlue1",
             fg="Black",
             font = ("Times New Roman",50) )
e.pack()



#textba/input bar - copy and paste text
def printInput():
    userInput = inputtxt.get(1.0,"end-1c",)
    lbl.config(text="Summarized Input: " + userInput)
#textbox creation
inputtxt = tk.Text(root, height = 30, width = 60)
inputtxt.pack()

#label creation

lbl = tk.Label(root,text = "")
lbl.pack()







#creating button

def button_clicked():

    print("Clicked Button!")
    inp = inputtxt.get(1.0, "end-1c")
    lbl.config(text = "Summarized input: "+inp)
    #debugging purposes



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
button.pack(padx = 20, pady = 20)



#quit with esc bar
root.bind('<Escape>', lambda e: quit_root(e))
def quit_root(e):
    root.destroy()
#start GUI
root.mainloop()

#implement scroll if text is long - button goes off of page -
# make the textbox output scrolling



#button click- triggers AI process aka ronan



