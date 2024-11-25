# File: calc.py
# =-=-=-=-=-=-=
# @author Joe Robertazzi - <tazzi@stanford.edu>
# Front end code that displays the app GUI

# Imports
from conversion import *
from tkinter import * 
from tkinter.ttk import *
import time

window = Tk()
window.title("jalc 1.0")
window.geometry("600x400")

window.minsize(300, 200)
window.maxsize(900, 600)

label = Label(window, text = "Enter text here:")
label.pack()

text_box = Entry(window)
text_box.pack()

def get_text():
    text = text_box.get()
    return text

def update_output():
    # inp = get_text()
    # var_storage = {'e': math.e}
    # var_list = []
    # while inp.find("=") != -1:
    #     curr_var = inp[0: inp.find("=")]
    #     if curr_var != "":
    #         var_list.append(curr_var.strip())
    #     inp = inp[inp.find("=") + 1:]
    # inp = replace_vars(inp, var_storage)
    # inp = remove_letters(inp)
    # brackets = True
    # while not operators_removed(inp):
    #     if brackets:
    #         res = reduce_inner_brackets(inp, brackets)
    #         inp = res[0]
    #         brackets = res[1]
    #     else: inp = basic_operations(inp)
    # if inp == "":
    #     output = inp
    # elif float(int(float(inp))) == float(inp): output = int(float(inp))
    # else: output = inp
    # for var in var_list: var_storage[var] = output
    # label.config(text = output)
    label.config(text = get_text)
    # window.after(10, update_output)

button = Button(window, text = "Click!", command = get_text)
button.pack()

update_output()
window.mainloop()


# # Top level window 
# frame = Tk() 
# frame.title("TextBox Input") 
# frame.geometry('600x400') 
# # Function for getting Input 
# # from textbox and printing it  
# # at label widget 
# def printInput(): 
#     inp = inputtxt.get(1.0, "end-1c") 
#     lbl.config(text = "Provided Input: "+inp) 
  
# # TextBox Creation 
# inputtxt = Text(frame, 
#                    height = 5, 
#                    width = 20) 
  
# inputtxt.pack() 
  
# # Button Creation 
# printButton = Button(frame, 
#                         text = "Print",  
#                         command = printInput) 
# printButton.pack() 
  
# # Label Creation 
# lbl = Label(frame, text = "") 
# lbl.pack() 
# frame.mainloop()