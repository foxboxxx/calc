# File: conversion.py
# =-=-=-=-=-=-=-=-=-=
# @author Joe Robertazzi - <tazzi@stanford.edu>
# Backend code that converts inputted equations into simplest form 

# Imports
from parser import *
import numpy as np
import math
import re

# Constants
OPERATIONS = {'+', '-', '/', '*', '%', '(', ')', '=', '^', '!'}
KEY_WORDS = {'log'}
UNITS = {}

# (Setting constants to math values by default)
var_storage = {'e': math.e}

# Removes letters from the input
def remove_letters(user_input):
    res = ""
    for i in range(len(user_input)): 
        if user_input[i].isnumeric() or user_input[i] in OPERATIONS or user_input[i] == '.':
            res += user_input[i]
    return res

# Ignores comments by removing from equation
def remove_comments(user_input):
    comment_indices = [user_input.find("//"), user_input.find("#")]
    if comment_indices != [-1, -1]:
        comment_index = min(num for num in comment_indices if num != -1)
        user_input = user_input[0: comment_index]
    return user_input

# Replace all variables in equation with their corresponding stored values
def replace_vars(user_input, var_storage):
    # Replace variables with values
    for var in var_storage:
        # Offset variable needed to prevent infinite loop when found variable isn't valid for a swap
        offset = 0

        # Loop through entire string until all variable candidates checked
        while user_input[offset:].find(var) != -1:
            loc = user_input[offset:].find(var)
            offset_loc = loc + offset
            left = right = False

            # Check left side of variable
            if offset_loc == 0: left = True
            elif user_input[offset_loc - 1] == " " or user_input[offset_loc - 1] in OPERATIONS: left = True

            # Check right side of variable
            if offset_loc == len(user_input) - len(var): right = True
            elif user_input[offset_loc + len(var)] == " " or user_input[offset_loc + len(var)] in OPERATIONS: right = True

            # Replace valid variable with stored value
            if left and right:
                replacement = "(" + str(var_storage[var]) + ")"
                user_input = user_input.replace(var, replacement)

            # If found replacement ISN'T valid, only look at rest of the string
            else:
                offset += loc + len(var)
    
    # Return modified equation
    return user_input

# Input a string with an open bracket at the front - will return the index of the matching closing bracket
def find_closing_bracket(user_input):
    if user_input[0] != "(": 
        return -1
    offset = 1
    for i in range(1, len(user_input)):
        if user_input[i] == "(": offset += 1
        if user_input[i] == ")": offset -= 1
        if offset == 0: return i
    return len(user_input) - 1

# Condenses all functions into numerical form
def condense_mathematical_functions(user_input):
   # for func in KEY_WORDS:
        
        # offset = 0
        # start = user_input[offset:].lower().find(func)
        # while start != -1:
        #     # !!! - Make this a function in another file specially for different math functions - !!!
        #     if func == 'log':
        #         trail_loc = start + len(func) + offset
        #         closing_bracket = -1
        #         if trail_loc < len(user_input):
        #             if user_input[trail_loc].isnumeric() or user_input[trail_loc] == ".":
        #                 decimal_used = False
        #                 first_arg = ""
        #                 for i in range(trail_loc, len(user_input)):
        #                     if user_input[i] == ".":
        #                         if decimal_used == True:
        #                             break
        #                         else: decimal_used = True
        #             if user_input[trail_loc] == "(": 
        #                 closing_bracket = find_closing_bracket(user_input[trail_loc:])
        #             if closing_bracket != -1:
        #                 user_input = user_input[0:trail_loc] + "(" + reduce_all_operators(user_input[trail_loc: trail_loc + closing_bracket + 1], True) + ")" + user_input[trail_loc + closing_bracket + 1:]
        #                 offset += trail_loc + 2 + len(reduce_all_operators(user_input[trail_loc: trail_loc + closing_bracket + 1], True))
                
        #         # while trail_loc < len(user_input) and user_input[trail_loc].isnumeric():
        #         #     arg *= 10
        #         #     arg += float(user_input[trail_loc])
        #         #     trail_loc += 1
        #         # replacement = math.log(arg, base)
        #         # user_input = user_input[0:start] + str(replacement) + user_input[trail_loc:]
        #     start = user_input[offset:].lower().find(func)
    return user_input


# Main function where backend code is tested
def main():
    history = []

    # Loop through command responses --> removed later when converted to GUI
    while True:
        # Resulting output
        output = 0

        # Testing wtih terminal nput string for now
        inp = input("<Calculation> ")

        # Add calculation to history
        history.append(inp)

        # If invalid input, display nothing (parenthesis not balanced) --> DEPRECIATED
        # if not are_parenthesis_balanced(inp): 
        #     print()
        #     continue

        # Quit upon entering nothing
        if inp == "": break

        # Remove comments from consideration
        inp = remove_comments(inp)

        # Store new variables (maybe make function some time later)
        var_list = []
        while inp.find("=") != -1:
            curr_var = inp[0: inp.find("=")]
            if curr_var != "":
                var_list.append(curr_var.strip())
            inp = inp[inp.find("=") + 1:]

        # Replace all variables in the equation with their respective values
        inp = replace_vars(inp, var_storage)

        # --------------------------------------

        # Remove all spaces from string
        inp = inp.replace(" ", "")

        print(inp)

        # Function replacement
        # inp = condense_mathematical_functions(inp)

        # --------------------------------------
        # Remove letters from equation (remove later when adding in units / conversions!!!)
        #inp = remove_letters(inp)

        inp = parse(inp)

        # Empty edge case
        if inp == "" or inp == None: 
            print("")
            continue

        # If result is an integer, print the integer version
        elif float(int(float(inp))) == float(inp): output = int(float(inp))

        # Otherwise print the float
        else: output = inp

        # Set variables equal to calculation
        for var in var_list: var_storage[var] = output

        # Print out the resulting calculation
        print(output)

main()