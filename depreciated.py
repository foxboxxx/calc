# File: depreciated.py
# =-=-=-=-=-=-=-=-=-=
# @author Joe Robertazzi - <tazzi@stanford.edu>
# Functions from previous builts that were made obsolete

import numpy as np
import math
import re

OPERATIONS = {'+', '-', '/', '*', '%', '(', ')', '=', '^', '!'}

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

# Tests to see if a string is valid to be returned as an answer to an equation
def operators_removed(user_input):
    # Empty case
    if user_input == "": return True

    try:
        float(user_input)
        return True
    except:
        return False

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