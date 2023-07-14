import re
import math
from typing import List

from ._processing_math_expression import _remove_redundant_operators, _remove_spaces, _remove_plus_sign
from ._handler_math_expression import _find_operator_index, _slice_by_index, _check_parentheses, _convert_to_int_if_needed, _get_args_math_function, _string_to_numeric
from ._eval_math_expression_error import EvalMathExpressionError

def __math_function(math_expression: str) -> int | float:
    i_ = math_expression.find('(')
    math_func = math_expression[:i_]
    args = map(__eval_math_recursive, _get_args_math_function(math_expression[i_+1:-1]))
    match math_func:
        # sqrt and abs
        case 'sqrt':
            return math.sqrt(*args)
        case 'abs':
            return math.fabs(*args)

        # floor and ceil
        case 'floor':
            return math.floor(*args)
        case 'ceil':
            return math.ceil(*args)

        # degrees and radians
        case 'deg':
            return math.degrees(*args)
        case 'rad':
            return math.radians(*args)

        # trigonometric functions
        case 'sin':
            return math.sin(*args)
        case 'cos':
            return math.cos(*args)
        case 'tan':
            return math.tan(*args)

        # inverse trigonometric functions
        case 'asin':
            return math.asin(*args)
        case 'acos':
            return math.acos(*args)
        case 'atan':
            return math.atan(*args)

        # hyperbolic functions
        case 'sinh':
            return math.sinh(*args)
        case 'cosh':
            return math.cosh(*args)
        case 'tanh':
            return math.tanh(*args)

        # inverse hyperbolic functions
        case 'asinh':
            return math.asinh(*args)
        case 'acosh':
            return math.acosh(*args)
        case 'atanh':
            return math.atanh(*args)

        # logarithmic functions
        case 'ln':
            return (lambda x: math.log(x))(*args)
        case 'log10':
            return math.log10(*args)
        case 'log':
            return (lambda x, y: math.log(x, y))(*args)

def __unary_operators(left_operand: str, operator: str, right_operand: str) -> int | float:
    match (left_operand, operator, right_operand):
        case ('', '-', right_operand): # minus sign
            return -__eval_math_recursive(right_operand)
        case (left_operand, '!', ''): # factorial
            if re.search('^[0-9]+$', left_operand): # check if left_operand is an integer
                return math.factorial(int(left_operand))
            elif re.search('^[0-9]+\.[0-9]+$', left_operand): # raises an exception if left_operand is a floating
                raise EvalMathExpressionError
            return math.factorial(__eval_math_recursive(left_operand))
        case (left_operand, '%', ''): # percentage
            return _convert_to_int_if_needed(__eval_math_recursive(left_operand)/100)

def __infix_operator(left_operand: str, operator: str, right_operand: str) -> int | float:
    match operator:
        case '+':
            return __eval_math_recursive(left_operand) + __eval_math_recursive(right_operand)
        case '-':
            return __eval_math_recursive(left_operand) - __eval_math_recursive(right_operand)
        case '*':
            return __eval_math_recursive(left_operand) * __eval_math_recursive(right_operand)
        case '/':
            return __eval_math_recursive(left_operand) / __eval_math_recursive(right_operand)
        case '^':
            return math.pow(__eval_math_recursive(left_operand), __eval_math_recursive(right_operand))

def __math_operator(math_expression: str, operator_index: int) -> int | float:
    left_operand, operator, right_operand = _slice_by_index(math_expression, operator_index)
    # unary operators
    result = __unary_operators(left_operand, operator, right_operand)
    if result != None:
        return result  
          
    # infix operator
    result = __infix_operator(left_operand, operator, right_operand)
    if result != None:
        return result
    
    raise EvalMathExpressionError

def eval_math(math_expression: str) -> int | float:
    math_expression = _remove_plus_sign(_remove_redundant_operators(_remove_spaces(math_expression)))
    if _check_parentheses(math_expression):
        return _convert_to_int_if_needed(__eval_math_recursive(math_expression))
    raise EvalMathExpressionError

def __eval_math_recursive(math_expression: str) -> int | float:
    if re.search('^[0-9]+,[0-9]+$', math_expression):
        raise EvalMathExpressionError

    # convert string to numeric
    number = _string_to_numeric(math_expression)
    if number != None:
        return number
    
    # remove external parentheses
    if math_expression[0] == '(' and math_expression[-1] == ')' and _check_parentheses(math_expression[1:-1]):
        return __eval_math_recursive(math_expression[1:-1])
    
    operator_index = _find_operator_index(math_expression)

    # math functions
    if operator_index == None:
        return __math_function(math_expression)
    
    # math operators
    return __math_operator(math_expression, operator_index)