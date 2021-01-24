# coding: utf8
"""
Utility methods that are used by the other files
but that do not directly change the given expression.
"""
from data import *



"""
Prints 'string' when DEBUG_LEVEL is higher 
than a required level.

@param string                   string, expression to print
@param debug_level_required     int, required level for debug printout
"""
def debug_print(string, debug_level_required):
    if DEBUG_LEVEL  >= debug_level_required:
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
    # bracket count for each bracket type
    bc = [0]*N_BRAC
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

