# File: parser.py
# =-=-=-=-=-=-=-=-=-=
# @author Joe Robertazzi - <tazzi@stanford.edu>
# Equation parser using the Shunting Yard Algorithm (implemented with my own personal additions)

# Imports
import numpy as np
import math
import re

OPERATORS = {'(' : 0, ')' : 0,
             '+' : 1, '-' : 1,
             '*' : 2, '/' : 2, 'mod' : 2,
             '^' : 3, 'log' : 3, 'ln' : 3, 'sqrt' : 3,
             'sin' : 3, 'cos' : 3, 'tan' : 3,
             '!' : 4
            }

RIGHT_ASSOCIATED = {'^'}

# Parses input into Reverse Poland Notation (RPN) using Shunting Yard Algorithm and solves string equations
def parse(user_input):
    output = ""
    stack = []
    i = 0
    # Cycle through input string
    while i < len(user_input):
        ch = ""
        while i < len(user_input) and ch not in OPERATORS.keys() and not user_input[i].isnumeric():
            if user_input[i] == " ": 
                ch = ""
            else: 
                ch += user_input[i]
            i += 1
        if ch in OPERATORS.keys(): i -= 1
        else: ch = user_input[i] 
            
        # Parse numeric term (including floating point numbers)
        if ch not in OPERATORS.keys():
            while i < len(user_input) and ch.isnumeric():
                output += ch
                i += 1
                if i < len(user_input): ch = user_input[i]
            if i < len(user_input) and ch == '.':
                output += ch
                i += 1
                if i < len(user_input): ch = user_input[i]
            while i < len(user_input) and ch.isnumeric():
                output += ch
                i += 1
                if i < len(user_input): ch = user_input[i]
            while i < len(user_input) and ch not in OPERATORS.keys():
                i += 1
                if i < len(user_input): ch = user_input[i]
            output += " "
        
        # Parse operator terms
        else:
            # Add operator to operator stack (unless closed parenthesis)
            if ch != ")": 
                while ch != "(" and len(stack) > 0 and OPERATORS[stack[len(stack) - 1]] >= OPERATORS[ch]:
                    if ch not in RIGHT_ASSOCIATED or OPERATORS[stack[len(stack) - 1]] > OPERATORS[ch]:
                        output += stack[len(stack) - 1] + " "
                        del stack[-1]
                    else:
                        break
                stack.append(ch)
            
            else:
                # If invalid match, return nothing
                if len(stack) == 0: 
                    return
                while len(stack) > 0:
                    if stack[len(stack) - 1] != "(":
                        output += stack[len(stack) - 1] + " "
                        del stack[-1]
                    else:
                        del stack[-1]
                        break
            i += 1

    # Add remaining operator stack to output string
    while len(stack) > 0:
        output += stack[len(stack) - 1] + " "
        del stack[-1]
    print("Output RPN: " + output)

    # Parse output string like a queue (FIFO)
    num_stack = []
    while output.find(" ") != -1:
        end = output.find(" ")
        curr = output[0:end]
        output = output[end + 1:]

        # Number adding
        if curr not in OPERATORS.keys():
            num_stack.append(curr)

        # Operations
        elif curr in OPERATORS.keys():
            if len(num_stack) > 0: right = num_stack.pop()
            else: continue

            # Basic operations
            if curr in {'+', '-', '/', '*', '^', 'log'}:
                if len(num_stack) > 0: left = num_stack.pop()
                else: 
                    num_stack.append(right)
                    continue
            if curr == "+":
                num_stack.append(str(float(left) + float(right)))
            elif curr == "-":
                num_stack.append(str(float(left) - float(right)))
            elif curr == "*":
                num_stack.append(str(float(left) * float(right)))
            elif curr == "/":
                num_stack.append(str(float(left) / float(right)))
            elif curr == "^":
                num_stack.append(str(float(left) ** float(right)))
            elif curr == "sin":
                num_stack.append(str(math.sin(float(right))))
            elif curr == "log":
                num_stack.append(str(math.log(float(right), float(left))))
    
    if len(num_stack) == 1:
        return num_stack[0]
    else:
        return
        