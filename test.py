# coding: utf8
"""
A couple of tests to verify 
if the programm works correctly.
"""

from data import *
from util import *
from brackets import *
from derive import *
from simplify import *
from syntax import *


# expressions for operator slit tests
expressions_operators = {
    "x^2" : "^",
    "x" : "^",
    "3*(2*x^4+3*x^4)+3*(2*x*sin{x}+x^2*cos{x})" : "+",
    "1+2+3+4+5" : "+",
    "log{x}*x" : "*",
    "log{x}*x*3*x^2" : "*"
}

# expressions for bracket removal test
expressions_brackets = [
    "((x))", "(((x)))",
    "(a+b)+(c*d)+(e*f)*(g+h)",
    "(x^2)", "(a+b)", "(a*b)", "((a*b))",
    "a*(b+c*d)", "a*(c*d+b)",
    "((3*x^2)*sin(x*(x^2)+exp(x))*cos(x))", 
    "0*x^2*(x^3+sin{x})+3*((2*x^1)*(x^3+sin{x})+x^2*cos{x})",
    "(sin(cos(exp(x^2))))",
    "((cos(sin(x)*exp(x))*((cos(x))*(exp(x))+(sin(x))*(exp(x)))))"
]

# expressions for simplification test
expressions_simplify = [
    "2^0",
    "x*x^3",
    "x^2*x^3",
    "2+x+5+3",
    "x^(-1)*1*x+5",
    "x*4*x^3*5+x^2*x*7",
    "3*(2*x^1*sin{x}+x^2*cos{x})",
    "(2*x^1*sin{x}+x^2*cos{x})",
    "(0*sin{x}*exp{1*x^0}+cos{x*0}*exp{x^0})", 
    "0*x^2*sin{x}+3*(2*x^1*sin{x}+x^2*cos{x})",
    "0*x^2*x^3+3*(2*x^1*x^3+x^2*3*x^2)+0*x^2*sin{x}+3*(2*x^1*sin{x}+x^2*cos{x})"
]

# derivatves tested with their solutions
expressions_functions = { 
    "sin(cos(exp(x^2)))" : "",
    "sin(x)*cos(x)*exp(x)" : "",
    "5*x" : "5",
    "x^2" : "2*x",
    "(5*x)^3" : "3*5^3*x^2",
    "(5*(x))^3" : "3*5^3*x^2",
    "5^3" : "0",
    "5^x" : "log(5)*exp(log(5)*x)",
    "x^x" : "x^x*(1+log(x))",
    "(sin(cos(exp(x^2))))" : "",
    "log(x^2)" : "2*x^-1",
    "sin(sin(x)*exp(x))" : "",
    "sinh(x)*sin(x)" : "",
    "sin(x)*sinh(x)" : "",
    "tanh(x)" : "1-(tanh(x))^2",
        "3*x^2*x^3" : "15*x^4",
    "3*x^2*sin(x)" : "6*x*sin(x)+3*x^2*cos(x)",
    "3*x^2*x^3+3*x^2*sin(x)" : "15*x^4+6*x*sin(x)+3*x^2*cos(x)",
    "3*x^2*(x^3+sin(x))" : "6*x*(x^3+sin(x))+3*x^2*(3*x^2+cos(x))" 
}


"""
Test method operator_split.

@param expr     string, expression to be tested
@param op       char, operator to split expression
"""
def test_operator_split(expr, op):
    print(LINE_STARS)
    print("Expression:\t" + expr)
    print("Operator:\t" + op)
    parts = operator_split(expr, op)
    print("Parts:")
    print(parts)
    print(LINE_STARS)
    

"""
Test bracket transformation and removal.

@param expr     string, expression to be tested
"""
def test_bracket_methods(expr):
    print(LINE_STARS)
    print("Expression:\t" + expr)
    expr = transform_brackets(expr)
    print("Transformed:\t" + transform_brackets(expr))
    expr = remove_brackets(expr)
    print("Removed:\t" + expr)
    print(LINE_STARS)


"""
Test bracket transformation and expression simplification.

@param expr     string, expression to be tested
"""
def test_simplification(expr):
    print(LINE_STARS)
    print("Expression:\t" + expr)
    expr = transform_brackets(expr)
    print("Removed:\t" + expr)
    expr = simplify_sub(expr)
    print("Simplified:\t" + expr)
    expr = simplify(expr)
    print("Simplified completely:\t" + expr)
    print(LINE_STARS)
    

"""
Test derive method in combination with other methods.

@param expr     string, expression to be tested
"""
def test_derive(expr, sol):
    print(LINE_STARS)
    derive(expr)
    print(LINE_STARS)
    print("Solution:\t" + sol)
    print(LINE_STARS)


"""
Printout at the beginning of a test block.

@param test     string, name of the test block
"""
def begin_test_block(test):
    print(LINE_STARS)
    print(LINE_STARS)
    print("TEST: " + test)
    print(LINE_STARS)


"""
Printout at the end of a test block.
"""
def end_test_block():
    print(LINE_STARS)
    print(LINE_STARS)
    print(NEWLINE)


"""
Main method. Prints the tests.
"""
def main():
    begin_test_block("OPERATOR SPLIT")

    for expr in expressions_operators:
        op = expressions_operators[expr]
        test_operator_split(expr, op)

    end_test_block()


    begin_test_block("BRACKET REMOVAL")

    for expr in expressions_brackets:
        test_bracket_methods(expr)

    end_test_block()


    begin_test_block("SIMPLIFY")

    for expr in expressions_simplify:
        test_simplification(expr)

    end_test_block()


    begin_test_block("DERIVATIVES")

    for expr in expressions_functions:
        sol = expressions_functions[expr]
        test_derive(expr, sol) 

    end_test_block()


# main method
main()
