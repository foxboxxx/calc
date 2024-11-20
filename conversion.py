import numpy as np

OPERATIONS = {'+', '-', '/', '*', '%', '(', ')', '[', ']', '{', '}', '=', '^', '!'}

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
def operators_removed(input):
    try:
        float(input)
        return True
    except:
        return False

# Main function where backend code is tested
def main():
    while True:
        # Testing wtih terminal nput string for now
        inp = input("Calculation: ")
        # Quit upon entering nothing
        if inp == "": break
        inp = remove_letters(inp)

        brackets = True
        # Cycle through all operators in string to reduce them one by one
        while not operators_removed(inp):
            # # Paranthesis calculations
            # original = inp
            # modified = False
            # if brackets:
            #     left_index = 0
            #     right_index = -1
            #     for i in len(inp):
            #         if inp[i] == '[': left_index = i
            #         if inp[i] == ']': 
            #             right_index = i
            #             break
            #     if right_index == -1 and left_index == 0: brackets = False
            #     else: 
            #         modified = True
            #         inp = inp[left_index:right_index]
            

            # Exponential calculations 
            power_index = inp.find("^")
            if power_index != -1:
                inp = condense_calculation(inp, power_index, "^")
                continue

            # Multiplication / division / modulus calculations  
            m_d_m_list = [inp.find("*"), inp.find("/"), inp.find("%")]
            if m_d_m_list != [-1, -1, -1]:
                m_d_m_index = min(num for num in m_d_m_list if num != -1)
                if m_d_m_index != -1:
                    inp = condense_calculation(inp, m_d_m_index, inp[m_d_m_index])
                    continue
            
            # Addition / subtraction
            a_s_list = [inp.find("+"), inp.find("-")]
            if a_s_list != [-1, -1]:
                a_s_index = min(num for num in a_s_list if num != -1)
                if a_s_index != -1:
                    inp = condense_calculation(inp, a_s_index, inp[a_s_index])
                    continue

        # If result is an integer, print the integer version
        if float(int(float(inp))) == float(inp):
            print(int(float(inp)))
        # Otherwise print the float
        else: 
            print(inp)

main()