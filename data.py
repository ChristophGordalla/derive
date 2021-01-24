# coding: utf8
"""
Data structures for the program.
"""



# argument for derivatives
ARG = "x"

# 'ARG_PLACEHOLD' is a placeholder in the derivative dictionary 'ELEM_FUNCTION_DEVS'
# to e.g. write log(x) : 1/x as log : ARG^(-1) in 'ELEM_FUNCTION_DEVS'
ARG_PLACEHOLD = "ARG"

# functions must be ordered in the following way:
# e.g. sinh must stand after sin,
# otherwise always 'sin' and not 'sinh' will be found
ELEM_FUNCTION_DEVS = { 
    "exp" : "exp", 
    "log" : ARG_PLACEHOLD+"^(-1)", 
    "sqrt" : "0.5*"+ARG_PLACEHOLD+"^(-0.5)", 
    "sin" : "cos", 
    "cos" : "(-1)*sin", 
    "tan" : "cos{"+ARG_PLACEHOLD+"}^(-2)", 
    "sinh" : "cosh", 
    "cosh" : "sinh", 
    "tanh" : "(1+(-1)*(tanh{"+ARG_PLACEHOLD+"})^2)"
}
ELEM_FUNCTIONS = list(ELEM_FUNCTION_DEVS.keys())

# for string replacements, with argument brackets {, }
ELEM_FUNCTION_VALS = {
    "sin{0}" : "0", 
    "sin{1}" : "1", 
    "cos{0}" : "1", 
    "cos{1}" : "0", 
    "exp{0}" : "1", 
    "exp{1}" : "e", 
    "log{1}" : "0", 
    "log{e}" : "1", 
    "sinh{0}" : "0", 
    "cosh{0}" : "1"
}

# list of operators for which a derivative rule has to be defined
# second dictionary entry is the operator precedence
OPERATORS_DICT = {"+" : 0, "-" : 0, "*" : 1, "^" : 2}
OPERATORS = list(OPERATORS_DICT.keys())

# brackets
BRACKETS = {"(" : ")", "{" : "}"}
BRACKETS_OPEN = list(BRACKETS.keys())
BRACKETS_CLOSED = list(BRACKETS.values())
N_BRAC = len(BRACKETS)

# replacements for syntax check
REPLACEMENTS = {
    "++" : "+", 
    "+-" : "-", 
    "-+" : "-", 
    "--" : "+", 
    "**" : "^", 
    "*+" : "*", 
    "^+" : "^"
}

# except for the replacements, 
# the following operator combinations
# are allowed and will be transformed
OPERATOR_COMBINATIONS = ["*+", "*-", "^+", "^-"]

# strings for printout
LINE_STARS = "**********************************************************************"
ERROR_SYNTAX = "ERROR: Invalid syntax in expression: "
NEWLINE = "\n"

# level for debug printout, 
# the higher, the more information, 
# 0 no printout at all
DEBUG_LEVEL = 1
