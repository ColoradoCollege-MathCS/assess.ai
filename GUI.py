import tkinter as tk
from tkinter import *
from pegasus import *
#from PIL import Image
#import sys
#print(sys.path)
#create main window

root = tk.Tk()

def pegasus_clicked():
	print("pegasus clicked!")
	root.destroy()

def LLM_zero_clicked():
	print("zero clicked!")
	root.destroy()

def LLM_one_clicked():
	print("one clicked!")
	root.destroy()

#image for Logo
image = PhotoImage(file = "logo.png")
image = image.zoom(5)
image = image.subsample(32)
panel = Label(root, image = image)

root.title("AssessAI")
root.configure(bg="SteelBlue1")
root.geometry("800x800")
#create a label/logo for main window
e = tk.Label(root, text = "Welcome to AssessAI, click anywhere to continue", bg="SteelBlue1",
             fg="Black",
             font = ("Times New Roman",30) )
e.pack()


#image label
image_lbl = tk.Label(root, image=image)
image_lbl.pack()


# buttons for the LLMs here
pegasus_button = tk.Button(root,
		text="Pegasus AI",
		command=pegasus_clicked,
		activebackground="blue",
		activeforeground="white",
		anchor="center",
		bd=3,
		bg="lightgray",
		disabledforeground="gray",
		fg="black",
		font=("Times New Roman", 12),
		height=2,
		highlightbackground="black",
		highlightcolor="green",
		justify="center",
		overrelief="raised",
		padx=10,
		pady=5,
		width=15,
		wraplength=50)

pegasus_button.pack(padx=20,pady=20)

LLM_zero_button = tk.Button(root,
		text="LLM 0",
		command=LLM_zero_clicked,
		activebackground="blue",
		activeforeground="white",
		anchor="center",
		bd=3,
		bg="lightgray",
		disabledforeground="gray",
		fg="black",
		font=("Times New Roman", 12),
		height=2,
		highlightbackground="black",
		highlightcolor="green",
		justify="left",
		overrelief="raised",
		padx=10,
		pady=5,
		width=15,
		wraplength=50)

LLM_zero_button.pack(padx=20,pady=20)


LLM_one_button = tk.Button(root,
		text="LLM 1",
		command=LLM_one_clicked,
		activebackground="blue",
		activeforeground="white",
		anchor="center",
		bd=3,
		bg="lightgray",
		disabledforeground="gray",
		fg="black",
		font=("Times New Roman", 12),
		height=2,
		highlightbackground="black",
		highlightcolor="green",
		justify="center",
		overrelief="raised",
		padx=10,
		pady=5,
		width=15,
		wraplength=50)

LLM_one_button.pack(padx=20,pady=20)		

#if click, remove image
#def image_click(event):
#    image_lbl.destroy()
    #bigbutton.delete()


# root.bind("<Button-1>", image_click)






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

# create instance of pegasus model
pegasus_model = Pegasus()


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

#integrate AI code

def button_clicked():
     #debugging purposes
    print("Clicked Button!")

    # convert inputtxt to string
    input_str = inputtxt.get(1.0, "end-1c")

    # run through Pegasus
    tokenized = pegasus_model.tokenize (input_str) # tokenize
    summarized = pegasus_model.summarizer(tokenized) # summarize
    summary = pegasus_model.detokenize(summarized) # detokenize

    summary[0] = summary[0].replace ("<pad>", "")
    summary[0] = summary[0].replace ("</s>", "")
                             
   # inp = summary #.get(1.0, "end-1c")
    outputtxt.config(state=NORMAL)#bring back editing
    outputtxt.delete(1.0, END) #clear anuthing from prev
    outputtxt.insert(1.0, "Summarized input: " + summary[0])  #take out summarized input eventually
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



