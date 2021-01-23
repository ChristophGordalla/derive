# coding: utf8
"""
Checks for incorrect syntax of an expression
and corrects it whenever possible.
"""
from data import *
from util import *



"""
Applies the replacements 'REPLACEMENTS' from data.py
to expression. This should be done before 
the 'has_correct_syntax' method checks 
the expression for possible error 
"""
def modify_with_replacements(expr):
    for repl in REPLACEMENTS:
        expr = expr.replace(repl, REPLACEMENTS.get(repl))
    return expr


"""
Gets the position of the closing bracket
when brackets have to be add to an expression
after a certain operator, e.g. for x^-1 -> x^(-1).

@param expr     string, expression add brackets
@param pos_i    int, position of the opening bracket

@return         int, position of the closing bracket
"""
def get_pos_for_closing_bracket(expr, pos_i):
    pos_op_list = []
    
    # '^' should never result in a break, e.g.:
    # x*-1^2 -> x*(-1^2)
    # x^-1^2 -> x^(-1^2)
    operators = OPERATORS[:-1]
    # add '/' to get a break
    operators.append('/')
    
    
    for bracket_open in BRACKETS_OPEN:
    # only expressions with no operators 
    # at the end have passed the 'has_correct_syntax()' 
    # method that was run before
        if expr[pos_i+1] == bracket_open:
            # find closing bracket
            pos_f = get_closed_bracket_pos(expr, pos_i+1)
            return pos_f
    
    for op in operators:
        pos_op = get_pos_of_first_op(expr[pos_i+1:], op)
        if pos_op > -1:
            pos_op_list.append(pos_op)
    if pos_op_list:
        pos_f = pos_i+1+min(pos_op_list)
        return pos_f
    # if neither another operator nor another bracket have been found,
    # the closing bracket must be placed at the end of the expression
    return len(expr)


"""
Submethod of 'modify_signs_after_operators(expr)'. 
Changes combinations of *-SOME_EXPRESSION 
and ^-SOME_EXPRESSION to *(-SOME_EXPRESSION)
and to ^(-SOME_EXPRESSION) in a substring of 'expr'.

@param expr     string, expression to be modified
@param pos      int, position of first char 
                of subexpress of 'expr'

@return         modified expression
"""
def modify_signs_after_operators_sub(expr, pos):
    ops_left = ['*', '^']
    ops_right = ['+', '-']
    
    pos_op = -1
    pos_ops = []
    pos_i = -1
    pos_f = -1
    
    expr_sub = expr[pos:]
    
    for op_left in ops_left:    
        pos_op = expr_sub.find(op_left)
        if pos_op > -1:
            pos_ops.append(pos_op)
    if not pos_ops:
        return expr
    pos_op = min(pos_ops)
        
    # only expressions with no operators 
    # at the end have passed the 'has_correct_syntax()' 
    # method that was run before
    pos_i = pos_op+1
    ch = expr_sub[pos_i]
    for op_right in ops_right:
        if ch == op_right:
            pos_f = get_pos_for_closing_bracket(expr_sub, pos_i)
            break
    #wrap into brackets
    if pos_f > -1:
        expr_sub = expr_sub[:pos_i]+'('+expr_sub[pos_i:pos_f]+')'+expr_sub[pos_f:]
        expr = expr[:pos] + expr_sub
    
    return modify_signs_after_operators_sub(expr, pos+pos_op+1)


"""
Changes combinations of *-SOME_EXPRESSION 
and ^-SOME_EXPRESSION to *(-SOME_EXPRESSION)
and to ^(-SOME_EXPRESSION)

@param expr     string, expression to be modified

@return         string, modified expression
"""
def modify_signs_after_operators(expr):
    return modify_signs_after_operators_sub(expr, 0)


"""
Submethod of 'modify_division_operators(expr)'. 
Changes combinations of *-SOME_EXPRESSION 
and ^-SOME_EXPRESSION to *(-SOME_EXPRESSION)
and to ^(-SOME_EXPRESSION) in a substring of 'expr'.

@param expr     string, expression to be modified
@param pos      int, position of first char 
                of subexpress of 'expr'

@return         modified expression
"""
def modify_division_operators_sub(expr, pos):
    pos_op = -1
    pos_i = -1
    pos_f = -1
    
    expr_sub = expr[pos:]
    
    pos_op = expr_sub.find('/')
    
    # only expressions with no operators 
    # at the end have passed the 'has_correct_syntax()' 
    # method that was run before
    pos_i = pos_op+1
    
    if pos_op == -1:
        return expr
    
    pos_f = get_pos_for_closing_bracket(expr_sub, pos_op)
    
    if pos_f > -1:
        expr_sub = expr_sub[:pos_op]+'*('+expr_sub[pos_i:pos_f]+')^(-1)'+expr_sub[pos_f:]
        expr = expr[:pos] + expr_sub
    
    return modify_division_operators_sub(expr, pos+pos_op+1)
            
    
"""
Changes all division operators '/..' to '*(..)^-1' 

@param expr     string, expression to be modified

@return         string, modified expression
"""
def modify_division_operators(expr):
    return modify_division_operators_sub(expr, 0)


"""
Modifies the input expression, such as correcting
syntax errors or eliminating division operators.

@param expr     string, expression to be modified

@return         string, modified expression
"""
def modify_input(expr):
    expr = modify_division_operators(expr)
    expr = modify_signs_after_operators(expr)
    return expr
    

"""
Checks if there is a closing bracket to each 
open bracket in the expression 'expr'.

@param expr     string, expression to be checked

@return         boolean, 
                True if syntax is correct, 
                False otherwise
"""
def has_incorrect_bracket_syntax(expr):
    n_expr = len(expr)
    # bracket count for each bracket type
    bc = [0]*N_BRAC
    for i, ch in enumerate(expr):
        for j, bracket in enumerate(BRACKETS):
            if ch == bracket:
                bc[j] += 1
            elif ch == BRACKETS.get(bracket):
                bc[j] -= 1
    for i, _ in enumerate(BRACKETS):
        if bc[i] != 0:
            return True
    return False


"""
Checks if there are empty brackets 
in the expression 'expr'.

@param expr     string, expression to be checked

@return         boolean, 
                False if syntax is correct, 
                True otherwise
"""
def has_empty_brackets(expr):
    n_expr = len(expr)
    for i, ch in enumerate(expr):
        for bracket in BRACKETS:
            if ch == bracket:
                b_i = i
                b_f = get_closed_bracket_pos(expr, i)
                if b_f - b_i == 1:
                    return True
    return False


"""
Checks if a combination of two operators
is in the list 'OPERATOR_COMBINATIONS'
of data.py.

@param op1  char, first operator of combination
@param op2  char, second operator of combination

@return     boolean
            True if operator combination is allowed, 
            False otherwise
"""
def is_allowed_operator_combination(op1, op2):
    op_string = op1+op2
    for combination in OPERATOR_COMBINATIONS:
        if op_string == combination:
            return True
    return False


"""
Checks if there are erroneous combinations
of brackets and operators or operators and operators
in the given expression, e.g. '+)' or '-*'.

@param expr     string, expression to be checked

@return         boolean, 
                False if syntax is correct, 
                True otherwise
"""
def has_incorrect_operator_syntax(expr):
    n_expr = len(expr)
    # create a new temperary operator dict 
    # which also contains '/' and its precedence
    operators = OPERATORS_DICT
    operators['/'] = 1
    
    for i, ch in enumerate(expr):
        for op in operators:
            if ch == op:
                # if operator is at the end of expression
                # directly before a closing bracket
                if i == n_expr-1:
                    return True
                for bracket_closed in BRACKETS_CLOSED:
                    if expr[i+1] == bracket_closed:
                        return True
                # for two adjacent operators, only the combinations
                # from 'OPERATOR_COMBINATIONS' from data.py 
                # are allowed combinations (they will be handled later 
                # by the method 'modify_input(..)')
                for op2 in operators:
                    if expr[i+1] == op2:
                        if not is_allowed_operator_combination(op, op2):
                            return True
                # rules if operator is not a sign
                if operators.get(op) > 0:
                    # if operator is at the beginning of the expression
                    # or directly after an open bracket
                    if i == 0:
                        return True
                    for bracket_open in BRACKETS_OPEN:
                        if expr[i-1] == bracket_open:
                            return True
    return False


"""
Checks if the syntax of expression 'expr' is correct.

@param expr     string, expression to be checked

@return         boolean, 
                False if syntax is correct, 
                True otherwise
"""
def has_correct_syntax(expr):
    if has_incorrect_bracket_syntax(expr):
        return False
    if has_incorrect_operator_syntax(expr):
        return False
    if has_empty_brackets(expr):
        return False
    return True
