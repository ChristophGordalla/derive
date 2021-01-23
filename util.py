# coding: utf8
"""
Utility methods that are used by the other files
but that do not directly change the given expression.
"""
from data import *



"""
Prints 'string' when debug_level is higher 
than a required level.

@param string           string, expression to print
@param level_required   int, required level for debug printout
"""
def debug_print(string, level_required):
    if debug_level >= level_required:
        print(string)


"""
Tries to parse 'expr' to an int or a float.

@param expr     string, expression to parse

@return         either int, float or string depending whether 'expr' is parsable
"""
def parse_number(expr):
    try:
        num = int(expr)
        return num
    except ValueError:
        try:
            num = float(expr)
            return num
        except ValueError:
            return expr


"""
Splits 'expr' at position 'pos' and returns both parts.
The character at position 'pos' itself is not included 
in one of the parts.

@param expr     string, expression to split
@param pos      int, position to split

@return         string list of the splitted parts 
                or an empty list if 'pos' is not between 0 and N
"""
def split_left_right(expr, pos):
    n_expr = len(expr)
    if pos < 0 or pos > n_expr:
        return []
    return [expr[:pos], expr[pos+1:]]
    
    
"""
Checks if 'expr' contains the argument 'ARG'.

@param expr     string, expression to be checked

@return:        boolean, True if 'expr' contains 'ARG', False otherwise
"""
def is_arg_in_expr(expr):
    for i, ch in enumerate(expr):
        elem_func = get_elem_func(expr, i)
        if elem_func != "":
            i += len(elem_func)
            continue
        if ch == ARG:
            return True
    return False


"""
Checks if 'expr' is the argument 'ARG' itself

@param expr     string, expression to be checked

@return:        boolean, True if 'expr' is 'ARG', False otherwise
"""
def is_arg_expr(expr):
    if expr == ARG:
        return True
    return False


"""
Detects if 'expr' contains an the first character of an
elementary function at the position 'pos'.

@param pos:     int, position where to look for the beginning of an elementary function

@return:        string, elementary function that has been found, empty string if nothing could be found
"""
def get_elem_func(expr, pos):
    func_found = ""
    n_expr = len(expr)
    for func_elem in ELEM_FUNCTIONS:
        n_func = len(func_elem)
        if pos+n_func < n_expr:
            if func_elem == expr[pos : pos+n_func]:
                func_found = func_elem
    return func_found


"""
Gets the operators which are one character left to 'b_i' 
and one character right to 'b_f' in 'expr' (if there are any). 

@param b_i  int, position from where to look one character left
@param b_f  int, position from where to look one character right

@return     string array with operators   
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
Evaluates the precendence of "operator". If the operator is empty
for e.g. (5)*(x) -> 5*(x) -> 5*x, we can always simplify. That is why
an empty operator gets -1 as precedence:

@param operator     string, operator whose precendence should be evaluated

@return             int, precedence of the operator,
                    i.e.: empty operator: -1, '+/-': 0, '*': 1, '^':2, etc.
"""
def get_precedence(operator):
    for op in OPERATORS_DICT:
        if op == operator:
            return OPERATORS_DICT.get(op)
    return -1


"""
Finds the corresponding closed bracket to an given open bracket
by looking at "openBrackets" and "closedBrackets".

@param bracketOpened    char, open bracket
@return                 char, corresponding closed bracket or empty string
                        if no closed bracket could be found. This is the
                        case when no correct open bracket has been past to the
                        method.
"""
def get_closed_bracket(open_bracket_given):
    bracket_closed = BRACKETS.get(open_bracket_given)
    if bracket_closed == None:
        return ""
    return bracket_closed


"""
Finds the closing bracket if there is an opening bracket at 'pos' 
of an expression 'expr'

@param expr     string, expression to be looked at
@param pos      int, position of opening pos
@return         int, position of closing bracket
                -2 if there was no opening bracket at 'pos'
                -1 if no closing bracket could be found
"""
def get_closed_bracket_pos(expr, pos):
    countOpen = 0;
    bracket_open = expr[pos]
    bracket_closed = BRACKETS.get(bracket_open)
    if bracket_closed == "":
        return -2
    for i, ch in enumerate(expr[pos+1:], start=pos+1):
        if ch == bracket_open:
            countOpen += 1
        elif ch == bracket_closed:
            countOpen -= 1
        if countOpen == -1:
            return i
    return -1


"""
Gets the position of the first occurance of an operator 'op' 
within an expression 'expr' that is NOT enclosed by brackets.

@param expr     string, expression to be analyzed
@param op       char, operator to look for

@return         int, first occurance of 'op' in 'expr'
                -1 if the 'op' did not occur in 'expr' 
                or if it is enclosed by bracket
"""
def get_pos_of_first_op(expr, op):
    n_expr = len(expr)
    n_brac = len(BRACKETS_OPEN)
    # bracket count for each bracket type
    bc = [0]*n_brac
    for i, ch in enumerate(expr):
        for j, bracket in enumerate(BRACKETS):
            if ch == bracket:
                bc[j] += 1
            elif ch == BRACKETS.get(bracket):
                bc[j] -= 1
        if ch == op:
            op_is_not_inside_brackets = True
            for j, _ in enumerate(BRACKETS):
                if bc[j] > 0:
                    op_is_not_inside_brackets = False
                    break
            if op_is_not_inside_brackets:
                return i
    return -1


"""
Gets the position of all operators 'op' 
within an expression 'expr' that are NOT enclosed by brackets.

@param expr     string, expression to be analyzed
@param op       char, operator to look for

@return         int list, list of operator positions
"""
def get_pos_of_all_ops(expr, op):
    n_expr = len(expr)
    i = 0
    positions = []
    while (i<n_expr):
        pos = get_pos_of_first_op(expr[i:], op)
        if pos == -1:
            break
        positions.append(i+pos)
        i += pos + 1
    
    return positions


"""
Finds the position of the first 'outer' operator of 'expr',
starting with the operator with lowest precedence ('+')
e.g. a*b+c*d returns 3, the position of '+'.

@param expr     string, expression to be searched

@return         int, position of the found operator,
                -1 when no operator has been found
"""
def get_pos_of_first_lowest_precedence_op(expr):
    pos = -1
    precedence_last = 10
    precedence_now = 10
    positions = []
    for op in OPERATORS_DICT:
        pos = get_pos_of_first_op(expr, op)
        if pos == -1:
            continue
        precedence_last = precedence_now 
        precedence_now = OPERATORS_DICT.get(op) 
        if precedence_now > precedence_last:
            break
        positions.append(pos)
    if positions:
        return min(positions)        
    return -1

