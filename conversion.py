import numpy as np

OPERATIONS = {'+', '-', '/', '*', '%', '(', ')', '[', ']', '{', '}', '=', '^', '!', '.'}

# Removes letters from the input
def remove_letters(user_input):
    res = ""
    for i in range(len(user_input)): 
        if user_input[i].isnumeric() or user_input[i] in OPERATIONS:
            res += user_input[i]
    return res

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

def main():
    while True:
        # Testing wtih terminal nput string for now
        inp = input("Calculation: ")
        # Quit upon entering nothing
        if inp == "": break
        inp = remove_letters(inp)

        res = temp = 0
        curr = ""

        while not inp.isnumeric():
            power_index = inp.find("^")
            if power_index != -1:
                vals = find_numerical(inp, power_index)
                prior = inp[0:power_index - len(vals[0])] 
                post = inp[power_index + len(vals[1]) + 1:]
                new = str(pow(int(vals[0]), int(vals[1])))
                inp = prior + new + post
                break

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