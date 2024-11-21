from tkinter import *
from tkinter.ttk import *

# Top level window 
frame = Tk() 
frame.title("TextBox Input") 
frame.geometry('600x400') 
# Function for getting Input 
# from textbox and printing it  
# at label widget 
def printInput(): 
    inp = inputtxt.get(1.0, "end-1c") 
    lbl.config(text = "Provided Input: "+inp) 
  
# TextBox Creation 
inputtxt = Text(frame, 
                   height = 5, 
                   width = 20) 
  
inputtxt.pack() 
  
# Button Creation 
printButton = Button(frame, 
                        text = "Print",  
                        command = printInput) 
printButton.pack() 
  
# Label Creation 
lbl = Label(frame, text = "") 
lbl.pack() 
frame.mainloop()