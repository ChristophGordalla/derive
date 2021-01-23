# coding: utf8
"""
*****************************************************
This is a little program to get analytical 
derivatives of expressions. Start the program
with python3 ui.py and follow the instructions
on the screen.

@author:    Christoph Gordalla
@data:      2021-23-01
@version:   Python 3.6.8 or higher
*****************************************************
"""
import sys

from data import *
from util import *
from brackets import *
from derive import *
from simplify import *
from syntax import *



"""
Prints the instructions at the start of the program.
"""
def print_instructions():
    print(LINE_STARS)
    print("Use this programm to derive analytic expressions.")
    print("The argument to derive is " + ARG, end='')
    print(" and the following functions are being recognized:" + NEWLINE)
    for elem_func in ELEM_FUNCTIONS:
        print(elem_func + "(" + ARG + ") ", end='')
    print(NEWLINE + NEWLINE + "Type 'quit' to exit the program.")
    print(LINE_STARS)
    print(NEWLINE)



"""
Computes the derivative of 'expr' and 
performs the necessary transformations
and simplifications.

@param expr     string, expression to be derived

@return         string, derivative of 'expr'
"""
def derive_ui(expr):
    expr = transform_brackets(expr)
    debug_print("Transformed:\t\t" + expr, 1)
    expr = simplify(expr)
    debug_print("Simplified:\t" + expr, 1)
    expr = derive_sub(expr)
    debug_print("Derived:\t\t" + expr, 1)
    expr = remove_brackets(expr)
    debug_print("Removed:\t\t" + expr, 1)
    expr = simplify(expr)
    debug_print("Simplified:\t\t" + expr, 1)
    expr = back_transform_brackets(expr)
    debug_print("Backtransformed:\t" + expr, 1)
    return expr


"""
This must be done when exiting the program.
"""
def exit_ui(exit_code):
    print(NEWLINE)
    sys.exit(exit_code)  
    

"""
Main method. Prints the infinite loop.
"""
def main():
    print_instructions()
    while True:
        try:
            expr = input("Enter expression: \t")
            debug_print("Expression:\t\t" + expr, 1)
            if expr == "quit":
                exit_ui(0)
            # apply replacements before syntax check
            expr = modify_with_replacements(expr)
            
            if not has_correct_syntax(expr):
                print(NEWLINE + ERROR_SYNTAX + NEWLINE + expr + NEWLINE)
                continue
            expr = modify_input(expr)
            debug_print("Syntax mod:\t\t" + expr, 1)
            print("Derivative:\t\t" + derive_ui(expr) + NEWLINE)
        except KeyboardInterrupt:
            exit_ui(1)
        except Exception as e:
            print(e)
            exit_ui(1)


# main method:
main()
