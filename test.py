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

import unittest



class TestsForDerivative(unittest.TestCase):
    # expressions for operator slit tests
    expressions_operators = {
        ("x^2", "^") : ('x', '2'),
        ("x", "^") : ('x'),
        ("3*(2*x^4+3*x^4)+3*(2*x*sin{x}+x^2*cos{x})", "+") : (['3*(2*x^4+3*x^4)', '3*(2*x*sin{x}+x^2*cos{x})'], []),
        ("1+2+3-4+5", "+") : (['1', '2', '3', '5'], ['4']),
        ("1+2+3-4+5", "-") : (['1', '2', '3', '5'], ['4']),
        ("log{x}*x", "*") : ('log{x}', 'x'),
        ("log{x}*x*3*x^2", "*") : ('log{x}', 'x', '3', 'x^2')
    }

    # expressions for bracket removal test
    expressions_brackets = {
        "((x))" : "x", 
        "(((x)))" : "x",
        "(a+b)+(c*d)+(e*f)*(g+h)" : "a+b+c*d+e*f*(g+h)",
        "(x^2)" : "x^2", 
        "(a+b)" : "a+b", 
        "(a*b)" : "a*b", 
        "((a*b))" : "a*b",
        "a*(b+c*d)" : "a*(b+c*d)", 
        "a*(c*d+b)" : "a*(c*d+b)",
        "((3*x^2)*sin{x*(x^2)+exp{x}}*cos{x})" : "3*x^2*sin{x*x^2+exp{x}}*cos{x}", 
        "0*x^2*(x^3+sin{x})+3*((2*x^1)*(x^3+sin{x})+x^2*cos{x})" : "0*x^2*(x^3+sin{x})+3*(2*x^1*(x^3+sin{x})+x^2*cos{x})",
        "(sin{cos{exp{x^2}}})" : "sin{cos{exp{x^2}}}",
        "((cos{sin{x}*exp{x}}*((cos{x})*(exp{x})+(sin{x})*(exp{x}))))" : "cos{sin{x}*exp{x}}*(cos{x}*exp{x}+sin{x}*exp{x})"
    }

    # expressions for simplification test
    expressions_simplify = {
        "2^0" : "1",
        "x*x^3" : "x^4",
        "x^2*x^3" : "x^5",
        "2+x+5+3" : "x+10",
        "x^(-1)*1*x+5" : "6",
        "x*4*x^3*5+x^2*x*7" : "20*x^4+7*x^3",
        "3*(2*x^1*sin{x}+x^2*cos{x})" : "3*(2*x*sin{x}+x^2*cos{x})",
        "(2*x^1*sin{x}+x^2*cos{x})" : "2*x*sin{x}+x^2*cos{x}",
        "(0*sin{x}*exp{1*x^0}+cos{x*0}*exp{x^0})" : "e", 
        "0*x^2*sin{x}+3*(2*x^1*sin{x}+x^2*cos{x})" : "3*(2*x*sin{x}+x^2*cos{x})",
        "0*x^2*x^3+3*(2*x^1*x^3+x^2*3*x^2)+0*x^2*sin{x}+3*(2*x^1*sin{x}+x^2*cos{x})" : "3*(2*x^4+3*x^4)+3*(2*x*sin{x}+x^2*cos{x})"
    }

    # derivatves tested with their solutions
    expressions_derivatives = { 
        "sin{cos{exp{x^2}}}" : "cos{cos{exp{x^2}}}*((-1)*sin{exp{x^2}}*(exp{x^2}*(2*x^(1))))",
        "sin{x}*cos{x}*exp{x}" : "(cos{x})*(cos{x}*exp{x})+(sin{x})*(((-1)*sin{x})*(exp{x})+(cos{x})*(exp{x}))",
        "5*x" : "(0)*(x)+(5)*(1)",
        "x^2" : "2*x^(1)",
        "(5*x)^3" : "3*(5*x)^(2)*((0)*(x)+(5)*(1))",
        "tanh{x}" : "((1+(-1)*(tanh{(x)})^2))*(1)",
        "3*x^2*x^3+3*x^2*sin{x}" : "(0)*(x^2*x^3)+(3)*((2*x^(1))*(x^3)+(x^2)*(3*x^(2)))+(0)*(x^2*sin{x})+(3)*((2*x^(1))*(sin{x})+(x^2)*(cos{x}))",
        "3*x^2*(x^3+sin{x})" : "(0)*(x^2*(x^3+sin{x}))+(3)*((2*x^(1))*((x^3+sin{x}))+(x^2)*(3*x^(2)+cos{x}))" 
    }
    
    # (0)*(x^2*(x^3+sin{x}))+(3)*((2*x^(1))*((x^3+sin{x}))+(x^2)*(3*x^(2)+cos{x}))
    # tests for operator splitting
    def test_operator_split(self):
        for expr_op in self.expressions_operators:
            sol = list(self.expressions_operators.get(expr_op))
            expr = expr_op[0]
            op = expr_op[1]
            parts = operator_split(expr, op)
            with self.subTest():
                self.assertEqual(parts, sol)
            
    
    # tests for bracket removal
    def test_brackets(self):
        for expr in self.expressions_brackets:
            sol = self.expressions_brackets.get(expr)
            expr = remove_brackets(expr)
            with self.subTest():
                self.assertEqual(expr, sol)
    
    
    # tests for expression simplification
    def test_simplification(self):
        for expr in self.expressions_simplify:
            sol = self.expressions_simplify.get(expr)
            expr = transform_brackets(expr)
            expr = simplify(expr)
            with self.subTest():
                self.assertEqual(expr, sol)
    
    
    # tests for derivative
    def test_derivative(self):
        for expr in self.expressions_derivatives:
            sol = self.expressions_derivatives.get(expr)
            expr = derive_sub(expr)
            with self.subTest():
                self.assertEqual(expr, sol)
            
    
# main:
unittest.main()
