import numpy as np

OPERATIONS = {'+', '-', '/', '*', '%', '(', ')', '[', ']', '{', '}', '=', '^', '!', '.'}

def remove_letters(user_input):
    res = ""
    for term in range(len(user_input)): 
        if user_input[term].isnumeric() or user_input[term] in OPERATIONS:
            res += user_input[term]
    return user_input

def main():
    while True:
        inp = input("Calculation: ")
        remove_letters(inp)
        inp = inp.split()
        print(inp)


main()