# Imports
import numpy as np

# Constants
OPERATIONS = {'+', '-', '/', '*', '%', '(', ')', '=', '^', '!'}

# Removes letters from the input
def remove_letters(user_input):
    res = ""
    for i in range(len(user_input)): 
        if user_input[i].isnumeric() or user_input[i] in OPERATIONS or user_input[i] == '.':
            res += user_input[i]
    return res

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
    if prior_post_list[0] == '' or prior_post_list[1] == '':
        if prior_post_list[0] == '' and prior_post_list[1] != '': calculation = prior_post_list[1]
        elif prior_post_list[1] == '' and prior_post_list[0] != '': calculation = prior_post_list[0]
        else: calculation = ""
    
    # Operation calculations
    elif operation == "^":
        calculation = str(pow(float(prior_post_list[0]), float(prior_post_list[1])))
    elif operation == "*":
        calculation = str(float(prior_post_list[0]) * float(prior_post_list[1]))
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
    if user_input == "": return ""

    # Exponential calculations 
    power_index = user_input.find("^")
    if power_index != -1:
        user_input = condense_calculation(user_input, power_index, "^")
        return user_input

    # Multiplication / division / modulus calculations  
    m_d_m_list = [user_input.find("*"), user_input.find("/"), user_input.find("%")]
    if m_d_m_list != [-1, -1, -1]:
        m_d_m_index = min(num for num in m_d_m_list if num != -1)
        if m_d_m_index != -1:
            user_input = condense_calculation(user_input, m_d_m_index, user_input[m_d_m_index])
            return user_input
    
    # Addition / subtraction
    a_s_list = [user_input.find("+"), user_input.find("-")]
    if a_s_list != [-1, -1]:
        a_s_index = min(num for num in a_s_list if num != -1)
        if a_s_index != -1:
            user_input = condense_calculation(user_input, a_s_index, user_input[a_s_index])
            return user_input

# Calculate inner most brackets and return new equation
# def reduce_inner_brackets(user_input):
    

# Main function where backend code is tested
def main():
    while True:
        # Testing wtih terminal nput string for now
        inp = input("Calculation: ")

        # Quit upon entering nothing
        if inp == "": break
        inp = remove_letters(inp)

        # Initialize assuming parenthesis exist
        brackets = True

        # Cycle through all operators in string to reduce them one by one
        while not operators_removed(inp):
            # Paranthesis in inputted equation
            if brackets:
                # Set indices for left and right brackets to be -1
                left_index = right_index = -1

                # Search the string for bracket pairs
                for i in range(len(inp)):
                    if inp[i] == '(': 
                        left_index = i
                    if inp[i] == ')': 
                        right_index = i
                        break

                # If no bracket pairs found, use PEMDAS as normal
                if right_index == -1 and left_index == -1: 
                    brackets = False

                # Otherwise, PEMDAS on inner-most brackets and then re-insert new value into original equation
                else: 
                    # Edge case for no closing bracket
                    if right_index == -1: right_index = len(inp)
                    inner_inp = inp[left_index + 1: right_index]

                    # Solve all operations for inner bracket
                    while not operators_removed(inner_inp):
                        inner_inp = basic_operations(inner_inp)

                    # Edge case for if there is no open bracket (just closing bracket)
                    if left_index == -1: left_index = 0
                    inp = inp[0: left_index] + inner_inp + inp[right_index + 1: len(inp)]
                    
            # No parenthesis in equation
            else:
                inp = basic_operations(inp)


        # Empty edge case
        if inp == "": print("")
        # If result is an integer, print the integer version
        elif float(int(float(inp))) == float(inp):
            print(int(float(inp)))
        # Otherwise print the float
        else: 
            print(inp)

main()