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
# OPERATIONS = {'+', '-', '/', '*', '%', '(', ')', '=', '^', '!'}
# KEY_WORDS = {'log'}
UNITS = {}

# (Setting constants to math values by default)
var_storage = {'e': math.e, 'pi': math.pi}

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

# Fixes back to back parenthesis so that they multiply instead of doing nothing
def add_parenthesis_multiplication(user_input):
    # # Fix situation with )( using regex substitution
    # user_input = re.sub(r"((?<!log)\(.*)\)\(", r"\1)*(", user_input)

    # # Fix situation with num( using regex substitution
    # user_input = re.sub(r"(\d)\(", r"\1*(", user_input)

    # # Fix situation with )num using regex substitution
    # user_input = re.sub(r"\)(\d)", r")*\1", user_input)

    # Return fixed string
    return user_input

# Replace all variables in equation with their corresponding stored values
def replace_vars(user_input, var_storage):
    # Check for edge case where the string is empty
    if user_input == "" or user_input == None: return

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
            elif user_input[offset_loc - 1] == " " or user_input[offset_loc - 1] in OPERATORS: left = True

            # Check right side of variable
            if offset_loc == len(user_input) - len(var): right = True
            elif user_input[offset_loc + len(var)] == " " or user_input[offset_loc + len(var)] in OPERATORS: right = True

            # Replace valid variable with stored value
            if left and right:
                replacement = "(" + str(var_storage[var]) + ")"
                user_input = user_input.replace(var, replacement)

            # If found replacement ISN'T valid, only look at rest of the string
            else:
                offset += loc + len(var)
    
    # Return modified equation
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

        # Fix back-to-back parenthesis
        inp = add_parenthesis_multiplication(inp)

        # Replace all variables in the equation with their respective values
        inp = replace_vars(inp, var_storage)

        print(inp)

        # Parses equation using Shunting Yard Algorithm and returns result
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