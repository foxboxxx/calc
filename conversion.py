# File: conversion.py
# =-=-=-=-=-=-=-=-=-=
# @author Joe Robertazzi - <tazzi@stanford.edu>
# Backend code that converts inputted equations into simplest form 

# Imports
import numpy as np
import math

# Constants
OPERATIONS = {'+', '-', '/', '*', '%', '(', ')', '=', '^', '!'}
KEY_WORDS = {'log'}
UNITS = {}

# (Setting constants to math values by default)
var_storage = {'e': math.e}

# Basic check before calculations (make sure parenthesis are balanced)
def are_parenthesis_balanced(user_input):
    # Initialize stack
    stack = []

    # Loop through string to make sure that parenthesis match
    for ch in user_input:
        if ch == ")":
            if len(stack) == 0: return False
            else: stack.pop()
        elif ch == "(": stack.append(ch)
        else: continue

    # Return whether parenthesis are balanced
    if len(stack) == 0: return True
    else: return False

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

# Isolates numerical parts of an equation at a given index
def find_numerical(user_input, index):
    b_index = index - 1
    a_index = index + 1
    before = after = ""
    while b_index >= 0 and user_input[b_index] not in OPERATIONS:
        before = user_input[b_index] + before
        b_index -= 1
    while a_index < len(user_input) and user_input[a_index] not in OPERATIONS:
        after += user_input[a_index]
        a_index += 1
    return [before, after]

# Breaks down a single oepration into a number, removing the operator from the string
def condense_calculation(user_input, index, operation):
    calculation = ""

    # Setting up calculation
    prior_post_list = find_numerical(user_input, index)
    prior = user_input[0:index - len(prior_post_list[0])] 
    post = user_input[index + len(prior_post_list[1]) + 1:]
    
    # Edge case for only one side of the operation has any value
    if prior_post_list[0] == '' or (prior_post_list[1] == '' and operation != "!"):
        if prior_post_list[0] == '' and prior_post_list[1] != '': calculation = prior_post_list[1]
        elif prior_post_list[1] == '' and prior_post_list[0] != '' and operation != "!": calculation = prior_post_list[0]
        else: calculation = ""
    
    # Operation calculations
    elif operation == "^":
        calculation = str(pow(float(prior_post_list[0]), float(prior_post_list[1])))
    elif operation == "*":
        calculation = str(float(prior_post_list[0]) * float(prior_post_list[1]))
    elif operation == "!":
        calculation = str(math.factorial(int(float(prior_post_list[0]))))
    elif operation == "/":
        calculation = str(float(prior_post_list[0]) / float(prior_post_list[1]))
    elif operation == "%":
        calculation = str(float(prior_post_list[0]) % float(prior_post_list[1]))
    elif operation == "+":
        calculation = str(float(prior_post_list[0]) + float(prior_post_list[1]))
    elif operation == "-":
        calculation = str(float(prior_post_list[0]) - float(prior_post_list[1]))
    return prior + calculation + post

# Tests to see if a string is valid to be returned as an answer to an equation
def operators_removed(user_input):
    # Empty case
    if user_input == "": return True

    try:
        float(user_input)
        return True
    except:
        return False

# Reduce a single operation from a basic string equation
def basic_operations(user_input):
    # Edge case for empty input:
    if user_input == "" or user_input == None: return ""

    # Exponential calculations 
    power_index = user_input.find("^")
    if power_index != -1:
        user_input = condense_calculation(user_input, power_index, "^")
        return user_input

    # Multiplication / division / modulus / factorial calculations  
    m_d_m_f_list = [user_input.find("*"), user_input.find("/"), user_input.find("%"), user_input.find("!")]
    if m_d_m_f_list != [-1, -1, -1, -1]:
        m_d_m_f_index = min(num for num in m_d_m_f_list if num != -1)
        user_input = condense_calculation(user_input, m_d_m_f_index, user_input[m_d_m_f_index])
        return user_input
    
    # Addition / subtraction
    a_s_list = [user_input.find("+"), user_input.find("-")]
    if a_s_list != [-1, -1]:
        a_s_index = min(num for num in a_s_list if num != -1)
        user_input = condense_calculation(user_input, a_s_index, user_input[a_s_index])
        return user_input

# Calculate inner most brackets and return new equation
def reduce_inner_brackets(user_input, brackets):
    # Set indices for left and right brackets to be -1
    left_index = right_index = -1

    # Search the string for bracket pairs
    for i in range(len(user_input)):
        if user_input[i] == '(': 
            left_index = i
        if user_input[i] == ')': 
            right_index = i
            break

    # If no bracket pairs found, use PEMDAS as normal
    if right_index == -1 and left_index == -1: 
        brackets = False

    # Otherwise, PEMDAS on inner-most brackets and then re-insert new value into original equation
    else: 
        # Edge case for no closing bracket
        if right_index == -1: right_index = len(user_input)
        inner_inp = user_input[left_index + 1: right_index]

        # Solve all operations for inner bracket
        while not operators_removed(inner_inp):
            inner_inp = basic_operations(inner_inp)

        # Edge case for if there is no open bracket (just closing bracket)
        if left_index == -1: left_index = 0

        # If closing bracket touches an open bracket, make sure values multiply
        if right_index + 1 < len(user_input) and user_input[right_index + 1] == "(": inner_inp += "*"

        # If previous character is a number, multiply the parenthesis by it
        if left_index > 0 and user_input[left_index - 1].isnumeric(): inner_inp = "*" + inner_inp

        # Edit user_input
        user_input = user_input[0: left_index] + inner_inp + user_input[right_index + 1:]
    
    return [user_input, brackets]
        
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

# Loops through entire string and removes all operators, resulting in a single value
def reduce_all_operators(user_input, brackets):
    # Cycle through all operators in string to reduce them one by one
    while not operators_removed(user_input):
        # Paranthesis in inputted equation
        if brackets:
            res = reduce_inner_brackets(user_input, brackets)
            user_input = res[0]
            brackets = res[1]

        # No parenthesis in equation
        else: user_input = basic_operations(user_input)
    
    # Update input
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
    for func in KEY_WORDS:
        offset = 0
        start = user_input[offset:].lower().find(func)
        while start != -1:
            # !!! - Make this a function in another file specially for different math functions - !!!
            if func == 'log':
                trail_loc = start + len(func) + offset
                closing_bracket = -1
                if trail_loc < len(user_input):
                    if user_input[trail_loc].isnumeric() or user_input[trail_loc] == ".":
                        decimal_used = False
                        first_arg = ""
                        for i in range(trail_loc, len(user_input)):
                            if user_input[i] == ".":
                                if decimal_used == True:
                                    break
                                else: decimal_used = True
                    if user_input[trail_loc] == "(": 
                        closing_bracket = find_closing_bracket(user_input[trail_loc:])
                    if closing_bracket != -1:
                        user_input = user_input[0:trail_loc] + "(" + reduce_all_operators(user_input[trail_loc: trail_loc + closing_bracket + 1], True) + ")" + user_input[trail_loc + closing_bracket + 1:]
                        offset += trail_loc + 2 + len(reduce_all_operators(user_input[trail_loc: trail_loc + closing_bracket + 1], True))
                
                # while trail_loc < len(user_input) and user_input[trail_loc].isnumeric():
                #     arg *= 10
                #     arg += float(user_input[trail_loc])
                #     trail_loc += 1
                # replacement = math.log(arg, base)
                # user_input = user_input[0:start] + str(replacement) + user_input[trail_loc:]
            start = user_input[offset:].lower().find(func)
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

        # If invalid input, display nothing (parenthesis not balanced)
        if not are_parenthesis_balanced(inp): 
            print()
            continue

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

        # Function replacement
        inp = condense_mathematical_functions(inp)

        # --------------------------------------
        # Remove letters from equation (remove later when adding in units / conversions!!!)
        inp = remove_letters(inp)

        # Remove all operators from calculation string
        inp = reduce_all_operators(inp, brackets = True)

        # Empty edge case
        if inp == "": 
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