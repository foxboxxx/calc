import numpy as np

OPERATIONS = {'+', '-', '/', '*', '%', '(', ')', '[', ']', '{', '}', '=', '^', '!', '.'}

# Removes letters from the input
def remove_letters(user_input):
    res = ""
    for term in range(len(user_input)): 
        if user_input[term].isnumeric() or user_input[term] in OPERATIONS:
            res += user_input[term]
    return res

def main():
    while True:
        # Test input string for now
        inp = input("Calculation: ")
        # Quit upon entering nothing
        if inp == "": break
        inp = remove_letters(inp)

        res = temp = 0
        curr = ""

        # Loop through all input characters
        for i in range(len(inp) + 1):
            # Enter arithmetic state if operation or at end of input
            if i == len(inp) or inp[i] in OPERATIONS:
                if curr != "":
                    # Adding
                    if curr == "+": 
                        res += temp
                        
                    # Subtracting
                    elif curr == "-": 
                        res -= temp

                    # Reset operator
                    if i != len(inp):
                        temp = 0
                        curr = inp[i]

                # As long as not the last element, set curr to new operator
                elif i != len(inp): 
                    curr = inp[i]
            else:
                if curr == "":
                    res *= 10
                    res += int(inp[i])
                else:
                    temp *= 10
                    temp += int(inp[i])
        print(res)

main()