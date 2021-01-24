# coding: utf8
"""
Methods to simplify an expression.
"""
import util
import brackets as br

from data import *



"""
Removes common elements from 'list_plus' and 'list_minus'.
set() cannot be used here since it is important
how often a certain element is shared between 
both lists.

@param list_plus    string list, first list
@param list_minus   string list, second list

@return             [list_plus, list_minus] with their 
                    common parts removed
"""
def remove_common_plus_minus_parts(list_plus, list_minus):
    tmp = list_minus[:]

    for e in list_plus:
        if e in list_minus:
            list_minus.pop(list_minus.index(e))
            
    for e in tmp:
        if e in list_plus:
            list_plus.pop(list_plus.index(e))
    
    # if both lists are empty, one of them must carry a zero
    if not list_plus and not list_minus:
        list_plus = ["0"]
    
    return [list_plus, list_minus]


"""
Simplfies a given list of expressions that are connected
through the '+' or '-' operator. 

@param parts_plus   string list, expressions that are connected
                    through the '+' operator
@param parts_minus  string list, expressions that are connected
                    through the '-' operator

@return             two string lists, simplified versions for 
                    'parts_plus' and 'parts_minus'
"""
def simplify_plus_minus_parts(parts_plus, parts_minus):
    parts_plus = simplify_addition_parts(parts_plus)
    parts_minus = simplify_addition_parts(parts_minus)
    
    # last element of simplified lists is the numerical sum or 0
    last_plus = util.parse_number(parts_plus.pop())
    util.debug_print(last_plus, 100)
    last_minus = util.parse_number(parts_minus.pop())
    util.debug_print(last_minus, 100)
    sum_number =  last_plus - last_minus
    if sum_number > 0:
        parts_plus.append(str(abs(sum_number)))
    elif sum_number < 0:
        parts_minus.append(str(abs(sum_number)))
    else:
        # only append a 0 summand to 'parts_plus'
        # if 'parts_plus' and 'parts_minus' 
        # are both empty lists
        if len(parts_plus) == 0 and len(parts_minus) == 0:
            parts_plus.append(str(abs(sum_number)))
    # if same parts are in parts_plus 
    # and in parts_minus, remove them from both lists
    # TODO: apply a distributive law in the future instead
    parts_plus, parts_minus = remove_common_plus_minus_parts(parts_plus, parts_minus)
    
    return [parts_plus, parts_minus]

    
"""
Splits an expression at its + and - signs.
E.g. "1+2+3-4+5" -> ['1', '2', '3', '5'], ['4']

@param expr     string, expression to be split

@return         two string lists, one with the parts that are
                connected through a plus sign, and one 
                with the parts that are connected through 
                a minus sign
"""
def operator_plus_minus_split(expr):
    parts_plus = []
    parts_minus = []
    n_expr = len(expr)
    sign = ''
    idx = 0
    part = ""
    # get sign of first summand
    sign = '+'
    if expr[0] == '-':
        sign = '-'
        idx = 1
        
    pos_all_plus = util.get_pos_of_all_ops(expr, '+')
    if sign == '-':
        pos_all_minus = util.get_pos_of_all_ops(expr[idx:], '-')
        pos_all_minus[:]=[i+1 for i in pos_all_minus]
    else:
        pos_all_minus = util.get_pos_of_all_ops(expr, '-')
    
    pos_all_ops = sorted([*pos_all_plus, *pos_all_minus])
    pos_all_ops.append(n_expr)
    
    for pos_op in pos_all_ops:
        part = expr[idx:pos_op]
        if sign == '+':
            parts_plus.append(part)
        elif sign == '-':
            parts_minus.append(part)
        if pos_op < n_expr:
            sign = expr[pos_op]
            idx = pos_op+1
    
    return [parts_plus, parts_minus]


"""
Splits an expression at any other operator than
+ or -.

@param expr     string, expression to be split
@param op       char, operator to split at

@return         string list with the parts that
                resulted from the split
"""
def operator_other_split(expr, op):
    parts = []
    pos_op = -1
    i = 0
    n_expr = len(expr)
    while i < n_expr:
        pos_op = util.get_pos_of_first_op(expr[i:n_expr], op)
        if pos_op != -1:
            parts.append(expr[i:i+pos_op])
            i += pos_op + 1
        else:
            parts.append(expr[i:n_expr])
            i = n_expr
    return parts


"""
Splits an expression 'expr' at the operator 'op'.

@param expr     string, expression to be split up
@param op       char, operator to split at

@return         string list with the splitted parts of 'expr'
"""
def operator_split(expr, op):
    if OPERATORS_DICT.get(op) == 0:
        parts = operator_plus_minus_split(expr)
    else:
        parts = operator_other_split(expr, op)
    
    return parts


"""
Splits an expression 'expr' at the operator with 
lowest precedence in that expression.

@param expr     string, expression to be split

@return         string array with the splitted parts of 'expr'
                or a list with only 'expr' if no split was possibles
"""
def lowest_precedence_operator_split(expr):
    parts = []
    offset = 0
    pos = util.get_pos_of_first_lowest_precedence_op(expr)
    # in this case not an operator, but a sign has been found
    if pos == 0:
        offset = 1
        pos = util.get_pos_of_first_lowest_precedence_op(expr[1:])
    if pos == -1:
        return [expr]
    op = expr[pos+offset]
    parts = operator_split(expr, op)
    return op, parts


"""
Sorts a list of parts with parts that are numbers
in the first place, then parts that are elemental
function in the order of the list ELEM_FUNCTIONS,
and then the other parts Submethod to be called
recursively from the method without suffix _sub.

@param parts    string list, list of parts to order

@return         string list, list of sorted parts
"""
def sort_string_parts_sub(parts):
    # first sort list with sorted() function,
    # this applies and alphabetical order AND
    # puts parts that are pure numbers in the beginning
    parts = sorted(parts)
    parts_sorted = []
    # then - to create a more natural order - 
    # sort the pre-ordered list according
    # to the order of the list ELEM_FUNCTIONS
    for elem_func in ELEM_FUNCTIONS:
        for part in parts:
            if part.startswith(elem_func):
                parts_sorted.append(part)
                parts.remove(part)
    # add the remaining parts to the sorted list
    for part in parts:
        parts_sorted.append(part)
    
    return parts_sorted 


"""
Sorts a list of parts with parts that are numbers
in the first place, then parts that are elemental
function in the order of the list ELEM_FUNCTIONS,
and then the other parts.

@param parts    string list, list of parts to order

@return         string list, list of sorted parts
"""
def sort_string_parts(parts):
    parts_new = sort_string_parts_sub(parts)
    if parts_new != parts:
        parts = parts_new
        parts_new = sort_string_parts(parts)
    return parts


"""
Simplfies a given list of expressions that are connected
through the '+' or '-' operator. 

@param parts    string list, expressions that are connected
                through the '+' or '-' operator
                
@return         string list, simplified expressions that are 
                connected through the '+' operator
"""
def simplify_addition_parts(parts):
    parts_simplified = []
    
    summand_number = 0
    
    for part in parts:
        summand_part = util.parse_number(part)
        if type(summand_part) != str:
            summand_number += summand_part
            continue
        parts_simplified.append(part)
    
    parts_simplified.append(str(summand_number))
    
    return parts_simplified


"""
Simplfies a given list of expressions that are connected
through the '*' operator. The list of expressions comes out sorted, 
with numbers being in the beginning of the list.

@param parts    string list, expressions that are connected
                through the '*' operator
                
@return         string list, simplified expressions that are 
                connected through the '*' operator
"""
def simplify_multiplication_parts(parts):
    parts_simplified = []
    
    parts_rest = []
    
    factor_number = 1
    
    potences = []
    exponent_number = 0
    exponent_string = ""
    exponent_string_parts = []
    
    for part in parts:
        factor_part = util.parse_number(part)
        if type(factor_part) != str:
            if factor_part == 0:
                return ["0"]
            factor_number *= factor_part
            continue
        if part == ARG:
            potences.append("1")
            continue
        part_sub = operator_split(part, "^")
        if len(part_sub) == 2 and part_sub[0].startswith(ARG):
            potences.append(part_sub[1])
            continue
        parts_rest.append(part)
    
    # add number first
    if factor_number != 1:
        parts_simplified.append(str(factor_number))
        
    # then add ARG^(..) terms
    for potence in potences:
        potence_parsed = util.parse_number(potence)
        
        if type(potence_parsed) == str:
            exponent_string_parts.append(potence_parsed)
        else:
            exponent_number += potence_parsed
    N_exponent_string_parts = len(exponent_string_parts)
    if N_exponent_string_parts > 0 and exponent_number > 0:
        exponent_string += "(" + "+".join(exponent_string_parts) + "+"
        exponent_string += str(exponent_number)
        exponent_string += ")"
        parts_simplified.append(ARG + "^" + exponent_string)
    elif N_exponent_string_parts > 0:
        exponent_string += "+".join(exponent_string_parts)
        if N_exponent_string_parts > 1:
            exponent_string = "(" + exponent_string + ")"
        parts_simplified.append(ARG + "^" + exponent_string)
    elif exponent_number > 0:
        if exponent_number == 1:
            parts_simplified.append(ARG)
        else:
            exponent_string = str(exponent_number)
            parts_simplified.append(ARG + "^" + exponent_string)
    elif exponent_number != 0:
        exponent_string = "(" + str(exponent_number) + ")"
        parts_simplified.append(ARG + "^" + exponent_string)
    
    # then add the other parts sorted
    parts_simplified += sort_string_parts(parts_rest) 
    
    # if the simplified list is emptry, the product is 1
    if not parts_simplified:
        parts_simplified = ["1"]
    
    return parts_simplified


"""
Simplfies a given list of expressions that are connected
through the '^' operator.

@param parts    string list, expressions that are connected
                through the '^' operator
                
@return         string list, simplified expressions that are 
                connected through the '^' operator
"""
def simplify_potential_parts(parts):
    num_first = util.parse_number(parts[0])
    if num_first == 1:
        return ["1"]
    
    # since ^ is not commutative, now only look at the last two parts
    # and let the recursion of 'simplify' do the magic 
    num_last = util.parse_number(parts[-1])
    num_pre_last = util.parse_number(parts[-2])
    
    if type(num_pre_last) != str and type(num_last) != str:
        return parts[:-2]+[str(num_pre_last ** num_last)]
    if num_pre_last == 1 or num_last == 0:
        if len(parts) > 2:
            return parts[:-2]
        else:
            return ["1"]
    if num_last == 1:
        return parts[:-1]
    if type(num_last) == str:
        return parts
    return parts


"""
Simplifies a given expression. Will later be called in a
recursive loop.

@param expr     string, expression to simplify

@return         string, simplified expression
"""
def simplify_sub(expr):
    util.debug_print("Simplify:\t"+expr, 10)
    expr_simp = ""
    parts_split = lowest_precedence_operator_split(expr)
    util.debug_print("After lowest Precedence operator split:", 100)
    util.debug_print(parts_split, 100)
    parts = []
    parts_plus = []
    parts_minus = []
    op = ""
    
    # if no split could be made, there are brackets, functions, or there is nothing to simplify
    if not len(parts_split) == 2:
        # look for brackets
        for bracket in BRACKETS:
            if expr[0] == bracket:
                expr_simp += bracket + simplify_sub(expr[1:-1]) + BRACKETS.get(bracket)     
                return expr_simp
        # look for functions
        elem_func = util.get_elem_func(expr, 0)
        if elem_func != "":
            expr_simp += elem_func + "{" + simplify_sub(expr[len(elem_func)+1:-1]) + "}"
            return expr_simp
        # if also no functions could be found, there is nothing to simplify
        return expr
    
    op = parts_split[0]
    parts = parts_split[1]
    if op == "+" or op == "-":
        parts_plus = parts[0]
        parts_minus = parts[1]
        parts_plus, parts_minus = simplify_plus_minus_parts(parts_plus, parts_minus)
        for part in parts_plus:
            expr_simp += simplify_sub(part) + '+'
        # remove last plus sign
        expr_simp = expr_simp[:-1]
        for part in parts_minus:
            expr_simp += '-' + simplify_sub(part)
    else:        
        if op == "*":
            parts = simplify_multiplication_parts(parts)
        elif op == "^":
            parts = simplify_potential_parts(parts)       
        for part in parts:
            expr_simp += simplify_sub(part) + op
        # remove last operator
        expr_simp = expr_simp[:-len(op)]
    return expr_simp


"""
Calls the simplify_sub method from above in a recursive procedure
until there is nothing more to simplify. 
It furthermore inserts the specific values 
from ELEM_FUNCTION_VALS in data.py.

@param expr     string, expression to simplify

@return         string, simplified expression
"""
def simplify(expr):
    for elem_func_val in ELEM_FUNCTION_VALS:
        expr = expr.replace(elem_func_val, ELEM_FUNCTION_VALS.get(elem_func_val))
    # remove brackets before starting
    # the other simplifications
    expr_simp = br.remove_brackets(expr)
    util.debug_print(expr_simp, 10)
    expr_simp = simplify_sub(expr_simp)
    # recursively repeat until 'simplify' does not change the string anymore
    if expr_simp == expr:
        return expr_simp
    return simplify(expr_simp)
