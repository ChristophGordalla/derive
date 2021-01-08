# coding: utf8
"""
Methods to derive an expression.
"""

from data import *
from util import *
from brackets import *
from derive import *
from simplify import *


"""
Creates a derivation string for the case that the exponent of a power law
expression is a number (double).

@param base:    string, the base of the power law
@param exp_num: double, exponent of power law

@return         string, derivative of power law
"""
def power_law_num(base, exp_num):
    # case x^0 = 1
    if exp_num == 0:
        return "0"
    # case x^1 = x
    if exp_num == 1:
        return "1"
    return str(exp_num)+"*"+base+"^"+"("+ str(exp_num-1)+")"


"""
Derives a power law expression base^exponent. 
'exponent' itself must not be dependent from
the argument to derive for.

@param base:        string, base expression of the power law
@param exponent:    string, exponential expression of the power law,
                    must not be dependent from the argument 'ARG' to derive for
                    
@return             string, derivative of power law
"""
def power_law_dev(base, exponent):
    try:
        exp_num = int(exponent)
        dev = power_law_num(base, exp_num)
    except ValueError:
        try:
            exp_num = float(exponent)
            dev = power_law_num(base, exp_num)
        # if 'exp' is not parseable to a float, just write down the analytic expression
        except ValueError:
            dev = exponent+"*"+base+"^"+"("+exponent+"-1)"
    return dev


"""
Derives 'expr' by using the sum rule, the product rule and the chain rule.
If it is not possible to derive any subexpression "devOf('subexpression')"
is written to the output string.

@param expr     string, expression to be derived

@return         string, derived expression
"""
def derive_sub(expr):
    debug_print("Derive:\t"+expr, 10)
    expr = remove_brackets(expr)
    if not is_arg_in_expr(expr):
        return "0"
    elif expr == ARG:
        return "1"
    derivative = ""
    offset = 0
    # if expr starts with a sign, add a '0' to its start
    if expr[0] == '+' or expr[0] == '-':
        expr = '0' + expr
    
    opPos = get_pos_of_first_lowest_precedence_op(expr)
    if opPos > -1:
        op = expr[opPos]
        [subexpr1, subexpr2] = split_left_right(expr, opPos)
        if op == "+":
            derivative += derive_sub(subexpr1) + "+" + derive_sub(subexpr2)
            return derivative
        if op == "-":
            # '-' sign in the in front of 'subexpr2' has been removed before, 
            # must be added again before applying 'swap_plus_and_minus_signs(..)'
            derivative += derive_sub(subexpr1) + "-(" + derive_sub(swap_plus_and_minus_signs("-"+subexpr2)) + ")"
            return derivative
        if op == "*":
            derivative += "(" + derive_sub(subexpr1) +")*(" + subexpr2 + ")"
            derivative += "+"
            derivative += "(" + subexpr1 +")*(" + derive_sub(subexpr2) + ")"
            return derivative
        if op == "^":
            if not is_arg_in_expr(subexpr1) and not is_arg_in_expr(subexpr2):
                derivative = "0"
                return derivative
            elif is_arg_in_expr(subexpr2):
                # convert to exp law and call derive again
                # a(x)^b(x) = exp(ln(a(x))*b(x))
                expr = "exp{log{" + subexpr1 + "}*" + subexpr2 + "}"
                derivative = derive_sub(expr)
                return derivative
            else:
                # a(x)^n
                if subexpr1 == ARG:
                    derivative = power_law_dev(subexpr1, subexpr2)
                else:
                    derivative = power_law_dev(subexpr1, subexpr2) + "*(" + derive_sub(remove_brackets(subexpr1))+ ")"
                return derivative
    # then scan 'expr' for chain rule
    for i in range(len(expr)):
        func = get_elem_func(expr, i)
        debug_print(func, 10)
        if func != "":
            idx_i = i+len(func)
            idx_f = get_closed_bracket_pos(expr, idx_i)
            # apply chain rule
            outer = ELEM_FUNCTION_DEVS.get(func)
            inner = expr[idx_i+1 : idx_f]
            # reminder 'ARG_PLACEHOLD' is a placeholder in the derivative dictionary
            # to e.g. write the entry log(x) : 1/x as log : ARG^(-1)
            posArg = outer.find(ARG_PLACEHOLD)
            if posArg > -1:
                while posArg > -1:
                    # replace all 'ARG_PLACEHOLD's from outer with '(inner)'
                    # add '(derive_sub(inner))' to string
                    outer = outer[0:posArg] + "(" + inner + ")" + outer[posArg+len(ARG_PLACEHOLD):len(outer)]
                    posArg = outer.find(ARG_PLACEHOLD)
                derivative += "(" + outer + ")" + "*" + "(" + derive_sub(inner) + ")"
                return derivative
            # outer derivative * inner derivative
            if inner == ARG:
                derivative += outer + "{" +ARG + "}"
            else:
                derivative += outer + "{" + inner+ "}" + "*" + "(" + derive_sub(inner) + ")"
            return derivative
    # then for everything else
    derivative += "d{" + expr + ", " + ARG + "}"
    return derivative


"""
Computes the derivative of 'expr' and 
performs the necessary transformations
and simplifications.

@param expr     string, expression to be derived

@return         string, derivative of 'expr'
"""
def derive(expr):
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
