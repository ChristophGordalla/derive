# coding: utf8
"""
Methods to transform the brackets of an expression.
"""
import util

from data import *



"""
Transforms argument bracket of elementary function
into curly brackets.

E.g.: sin(x) -> sin{x}

@param expr     string, expression to be modified

@return         string, modified expression
"""
def transform_brackets(expr):
    n_expr = len(expr)
    n_func = -1
    b_i = -1
    is_transformable = False
    for i, _ in enumerate(expr):
        elem_func = util.get_elem_func(expr, i)
        n_func = len(elem_func)
        if n_func > 0:
            b_i = i + n_func
            # if an elementary function has been found
            # and its following bracket has not yet been transformed
            # to '{', then break the loop and perform an transformation
            if b_i < n_expr and expr[b_i] == "(":
                is_transformable = True
                break
    if is_transformable:
        b_f = util.get_closed_bracket_pos(expr, b_i)
        return transform_brackets(expr[:b_i] + "{" + expr[b_i+1:b_f] + "}" + expr[b_f+1:])
    return expr    


"""
Back transforms curly brackets to round brackets.

@param expr     string, expression to be modified

@return         string, modified expression
"""
def back_transform_brackets(expr):
    expr = expr.replace("{", "(")
    expr = expr.replace("}", ")")
    return expr


"""
Evaluates the precendence of "operator". If the operator is empty
for e.g. (5)*(x) -> 5*(x) -> 5*x, we can always simplify. That is why
an empty operator gets -1 as precedence:

@param operator     char, operator whose precendence should be evaluated

@return             int, precedence of the operator,
                    i.e.: empty operator: -1, '+/-': 0, '*': 1, '^':2, etc.
"""
def get_precedence(operator):
    for op in OPERATORS_DICT:
        if op == operator:
            return OPERATORS_DICT.get(op)
    return -1


"""
Gets the operators which are one character left to 'b_i' 
and one character right to 'b_f' in 'expr' (if there are any). 

@param expr     string, expression to evaluate
@param b_i      int, position from where to look one character left
@param b_f      int, position from where to look one character right

@return         string array with operators   
"""
def get_left_right_ops(expr, b_i, b_f):
    op_left = ""
    op_right = ""
    n_expr = len(expr)
    for op in OPERATORS:
        if b_i > 0:
            if op == expr[b_i-1]:
                op_left = op
        if b_f < n_expr-1:
            if op == expr[b_f+1]:
                op_right = op
    return [op_left, op_right]


"""
Switches all '+' of an expression to '-' and vice versa 
if those signs are not enclosed by brackets.

@param expr     string, expression to be modified

@return         string, modified expression
"""
def swap_plus_and_minus_signs(expr):
    pos_plus = util.get_pos_of_all_ops(expr, '+')
    pos_minus = util.get_pos_of_all_ops(expr, '-')
    
    for pos in pos_plus:
        expr = expr[:pos] + '-' + expr[pos+1:]
    for pos in pos_minus:
        expr = expr[:pos] + '+' + expr[pos+1:]
    
    # if the first character is not a sign, 
    # add a minus in the beginning
    if expr[0] != '+' and expr[0] != '-':
        expr = '-' + expr

    return expr


"""
Recursively removes unnecessary brackets from an expression 'expr'.

@param expr     string, expression to be modified

@return         string, modified expression
"""
def remove_brackets(expr):
    util.debug_print("Remove brackets:\t"+expr, 10)
    n_expr = len(expr)
    op_left = ''
    op_right = ''
    is_bracket_pair_removable = True
    is_minus_sign_before_bracket = False
    
    for i, ch in enumerate(expr):
        if ch == "(":
            is_bracket_pair_removable = True
            b_i = i
            b_f = util.get_closed_bracket_pos(expr,i)
            # remove brackets if the whole expression is wrapped into brackets
            if b_i == 0 and b_f == n_expr-1:
                return remove_brackets(expr[b_i+1:b_f])
                
            op_left, op_right = get_left_right_ops(expr, b_i, b_f)
            if op_left == '-':
                is_minus_sign_before_bracket = True
            
            pos_lowest_precedence_op = util.get_pos_of_first_lowest_precedence_op(expr[b_i+1:b_f])
            # if there is no operator at all in 'expr',
            # then 'pos_lowest_precedence_op' is equal to -1 and
            # outer brackets can always be removed
            # except for the (sub-)expression "(-1)"
            if pos_lowest_precedence_op > -1:
                op_lowest_precedence = expr[b_i+1+pos_lowest_precedence_op]
                lowest_precendence = get_precedence(op_lowest_precedence)
                precedence_left = get_precedence(op_left)
                precedence_right = get_precedence(op_right)
                # '^' is right associative, so do not remove any brackets
                # when all operators are '^'
                if ((op_left == "^" or op_right == "^") and op_lowest_precedence == "^"):
                    is_bracket_pair_removable = False
                else:
                    # brackets cannot be removed if there is 
                    # an operator with lower precedence within the bracket pair
                    if(precedence_right > lowest_precendence or precedence_left > lowest_precendence):
                        is_bracket_pair_removable = False
            if is_minus_sign_before_bracket:
                expr = expr[:b_i-1] + swap_plus_and_minus_signs(expr[b_i+1:b_f]) + expr[b_f+1:]
                return remove_brackets(expr)
            if is_bracket_pair_removable:
                expr = expr[:b_i] + expr[b_i+1:b_f] + expr[b_f+1:]
                # if the operator before the bracket is a '+' 
                # and the sign of the first summand is a '-', 
                # then removing the brackets will result in '+-'
                # to occur in the beginning of the expression
                expr = expr.replace("+-", "-")
                return remove_brackets(expr)
    # if there are no brackets to be removed, just return 'expr'
    return expr
