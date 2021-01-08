# coding: utf8
"""
Methods to simplify an expression.
"""
from data import *
from util import *
from brackets import *



"""
Simplfies a given list of expressions that are connected
through the '+' or '-' operator. 

@param parts    string list, expressions that are connected
                through the '+' or '-' operator
@param sign     char, either '+' or '-'
                
@return         two string lists, 
                one list of simplified expressions 
                that are connected through the '+' operator,
                one list of simplified expressions 
                that are connected through the '-' operator,
"""
def simplify_plus_minus_parts(expr):
    parts_plus_sign = []
    parts_minus_sign = []
    n_expr = len(expr)
    sign = ''
    pos = 0
    i = 0
    part = ""
    # get sign of first summand
    sign = '+'
    if expr[0] == '-':
        sign = '-'
        i = 1
    # TODO: rewrite method with get_pos_of_all_ops()
    while (i<n_expr):
        pos_plus = get_pos_of_first_op(expr[i:], '+')
        pos_minus = get_pos_of_first_op(expr[i:], '-')
        # append whole expression as part 
        # when it neither contains a '+' nor a '-'
        if pos_plus == -1 and pos_minus == -1:
            part = expr[i:n_expr]
            if sign == '+':
                parts_plus_sign.append(part)
            elif sign == '-':
                parts_minus_sign.append(part)
            break
        # find out if a '+' or a '-' occurs first in 'expr'
        if pos_plus == -1:
            pos = pos_minus
        elif pos_minus == -1:
            pos = pos_plus
        elif pos_plus < pos_minus:
            pos = pos_plus
        else:
            pos = pos_minus
        # extract and append the corresponding part
        part = expr[i:i+pos]
        if sign == '+':
            parts_plus_sign.append(part)
        elif sign == '-':
            parts_minus_sign.append(part)
        sign = expr[i+pos]
        i += pos+1
    
    parts_plus_sign_simplified = simplify_addition_parts(parts_plus_sign, '+')
    parts_minus_sign_simplified = simplify_addition_parts(parts_minus_sign, '-')
    
    #TODO: if same parts are in parts_plus_sign_simplified 
    # and in parts_minus_sign_simplified, remove them from both lists
    
    # last element of simplified lists is the numerical sum or 0
    last_plus = parse_number(parts_plus_sign_simplified.pop())
    debug_print(last_plus, 100)
    last_minus = parse_number(parts_minus_sign_simplified.pop())
    debug_print(last_minus, 100)
    sum_number =  last_plus - last_minus
    if sum_number > 0:
        parts_plus_sign_simplified.append(str(abs(sum_number)))
    elif sum_number < 0:
        parts_minus_sign_simplified.append(str(abs(sum_number)))
    else:
        # only append a 0 summand to 'parts_plus_sign_simplified'
        # if 'parts_plus_sign_simplified' and 'parts_minus_sign_simplified' 
        # are both empty lists
        if len(parts_plus_sign_simplified) == 0 and len(parts_minus_sign_simplified) == 0:
            parts_plus_sign_simplified.append(str(abs(sum_number)))
    
    return [parts_plus_sign_simplified, parts_minus_sign_simplified]
    

"""
Splits an expression 'expr' at the operator 'op'.

@param expr     string, expression to be split up
@param op       char, operator to split at

@return         string array with the splitted parts of 'expr'
"""
def operator_split(expr, op):
    parts = []
    pos_op = -1
    i = 0
    n_expr = len(expr)
    while i < n_expr:
        pos_op = get_pos_of_first_op(expr[i:n_expr], op)
        if pos_op != -1:
            parts.append(expr[i:i+pos_op])
            i += pos_op + 1
        else:
            parts.append(expr[i:n_expr])
            i = n_expr
    return parts


"""
Splits an expression 'expr' at the operator 'op' 
into a maximum of 'maxsplit' parts.

@param expr         string, expression to be split up
@param op           char, operator to split at
@param maxsplit     int, maximum number of parts that the expression is split into
"""
def operator_max_split(expr, op, maxsplit):
    parts = operator_split(expr, op)
    n_parts = len(parts)
    parts_maxsplit = []
    part_last = ""
    
    for i in range(n_parts):
        if i < maxsplit-1:
            parts_maxsplit.append(parts[i])
        else:
            for j in range(i, n_parts):
                part_last += parts[j] + op 
            part_last = part_last[:-len(op)]
            parts_maxsplit.append(part_last)
            break
    
    return parts_maxsplit


"""
Splits an expression 'expr' at the operator with 
lowest precedence in that expression.

@param expr     string, expression to be split

@return         string array with the splitted parts of 'expr'
                or a list with only 'expr' if no split was possibles
"""
def lowest_precedence_operator_split(expr):
    parts = []
    first_char_is_sign = False
    pos = get_pos_of_first_lowest_precedence_op(expr)
    # in this case not an operator, but a sign has been found
    if pos == 0:
        first_char_is_sign = True
        pos = get_pos_of_first_lowest_precedence_op(expr[1:])
    if pos == -1:
        return [expr]
    if first_char_is_sign:
        op = expr[pos+1]
        parts = operator_split(expr, op)
    else:
        op = expr[pos]
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
    for elemFunction in ELEM_FUNCTIONS:
        for part in parts:
            if part.startswith(elemFunction):
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
@param sign     char, either '+' or '-'
                
@return         string list, simplified expressions that are 
                connected through the '+' operator
"""
def simplify_addition_parts(parts, sign):
    parts_simplified = []
    
    summand_number = 0
    
    for part in parts:
        summand_part = parse_number(part)
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
    parts_rest_sorted = []
    
    factor_number = 1
    
    potences = []
    exponent_number = 0
    exponent_string = ""
    exponent_string_parts = []
    
    for part in parts:
        factor_part = parse_number(part)
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
        potence_parsed = parse_number(potence)
        
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
Splits a part at the '*' operator into exactly two parts.

@param part     string, part to split

@return         string list, splitted parts
"""
def get_distributive_law_sub_parts(part):
    parts_sub = [""]*2
    parts_split = operator_max_split(part, "*", 2)
    debug_print(parts_split, 10)
    
    if (len(parts_split) == 1) or parts_split[0] == "":
        parts_sub[0] = "1"
        parts_sub[1] = parts_split[0]
        return parts_sub
        
    return parts_split


"""
Applies a distributive law to a list of summands.
The method looks for similar factors in the summands
and puts them outside the brackets ("ausklammern").

@param summnds  string list, list of summands
@param sign     char, either '+' or '-'

@return         string, summands in brackets 
                with distributive law applied
"""
# TODO: Currently unused. Use in future versions.
def left_distributive_law(summands, sign):
    summands_simplified = []
    summand_simplified = ""
    
    n_summands = len(summands)
    
    factor_right = ""
    
    summands_sub = []
    
    has_been_visited = [False]*n_summands
    has_been_simplified = False
    
    if n_summands == 1:
        return summands
    
    for i in range(n_summands):
        if has_been_visited[i]:
            continue
        has_been_simplified = False
        
        summands_sub = get_distributive_law_sub_parts(summands[i])
        
        factor_right = summands_sub[1]
        
        summand_simplified = "(" + summands_sub[0]
        
        for j in range(i+1, n_summands):
            if has_been_visited[j]:
                continue
            summands_sub = get_distributive_law_sub_parts(summands[j])
            
            if factor_right == summands_sub[1]:
                summand_simplified += sign + summands_sub[0]
                has_been_visited[j] = True
                has_been_simplified = True
                
            summand_simplified += ")*" + factor_right
            
        if has_been_simplified:
            summands_simplified.append(summand_simplified)
        else:
            summands_simplified.append(summands[i])
    
    return summands_simplified


"""
Simplfies a given list of expressions that are connected
through the '^' operator.

@param parts    string list, expressions that are connected
                through the '^' operator
                
@return         string list, simplified expressions that are 
                connected through the '^' operator
"""
def simplify_potential_parts(parts):
    num_first = parse_number(parts[0])
    if num_first == 1:
        return ["1"]
    
    # since ^ is not commutative, now only look at the last two parts
    # and let the recursion of 'simplify' do the magic 
    num_last = parse_number(parts[-1])
    num_pre_last = parse_number(parts[-2])
    
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
    debug_print("Simplify:\t"+expr, 10)
    expr_simp = ""
    parts_split = lowest_precedence_operator_split(expr)
    debug_print("After lowest Precedence operator split:", 100)
    debug_print(parts_split, 100)
    parts = []
    parts_plus = []
    parts_minus = []
    op = ""
    
    if len(parts_split) == 2:
        # both variables will be used after the if-else branch
        op = parts_split[0]
        parts = parts_split[1]
    # if no split could be made, there are brackets, functions, or there is nothing to simplify
    else:
        # look for brackets
        for k in range(N_BRAC):
            if expr[0] == BRACKETS_OPEN[k]:
                expr_simp += BRACKETS_OPEN[k] + simplify_sub(expr[1:-1]) + BRACKETS_CLOSED[k]     
                return expr_simp
        # look for functions
        elemFunc = get_elem_func(expr, 0)
        if elemFunc != "":
            n_func = len(elemFunc)
            expr_simp += elemFunc + "{" + simplify_sub(expr[n_func+1:-1]) + "}"
            return expr_simp
        # if also no functions could be found, there is nothing to simplify
        return expr
                
    if op == "+" or op == "-":
        parts = simplify_plus_minus_parts(expr)
        parts_plus = parts[0]
        parts_minus = parts[1]
    elif op == "*":
        parts = simplify_multiplication_parts(parts)
    elif op == "^":
        parts = simplify_potential_parts(parts)
    
    # splitting up the expression of the (simplified) parts from above
    if op == '+' or op == "-":
        for part in parts_plus:
            expr_simp += simplify_sub(part) + '+'
        # remove last plus sign
        expr_simp = expr_simp[:-1]
        for part in parts_minus:
            expr_simp += '-' + simplify_sub(part)
    else:
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
    expr_simp = remove_brackets(expr)
    debug_print(expr_simp, 10)
    expr_simp = simplify_sub(expr_simp)
    # recursively repeat until 'simplify' does not change the string anymore
    if expr_simp == expr:
        return expr_simp
    return simplify(expr_simp)
