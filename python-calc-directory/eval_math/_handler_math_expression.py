from typing import Tuple, List
import math
import re

def _slice_by_index(string: str, index: int) -> Tuple[str, str, str]:
    return string[:index], string[index], string[index+1:]

def _check_parentheses(string: str) -> bool:
    count = 0
    for i in string:
        if i == '(':
            count += 1
        elif i == ')':
            count -= 1
        if count < 0:
            return False
    if count > 0:
        return False
    return True

def _find_operator_index(math_expression: str) -> int | None:
    i_, i_continue, count = None, None, 0
    for i in range(len(math_expression)):
        if i == i_continue or math_expression[i] not in '+-*/^!%()':
            continue
        elif math_expression[i] == '(':
            count += 1
            continue
        elif math_expression[i] == ')':
            count -= 1
            continue
        if count == 0:
            if i+2 <= len(math_expression):
                if math_expression[i:i+2] in ('*-', '/-', '^-'):
                    i_continue = i+1
                elif math_expression[i:i+2] in ('!+', '!-', '!*', '!/', '!^', '%+', '%-', '%*', '%/', '%^'):
                    continue
            match (math_expression[i], None if i_ == None else math_expression[i_]):
                case ('+', '+' | '-' | '*' | '/' | '^' | '!' | '%' | None):
                    i_ = i
                case ('-', '+' | '-' | '*' | '/' | '^' | '!' | '%' | None):
                    i_ = i
                case ('*', '*' | '/' | '^' | '!' | '%' | None):
                    i_ = i
                case ('/', '*' | '/' | '^' | '!' | '%' | None):
                    i_ = i
                case ('^', '^' | '!' | '%' | None):
                    i_ = i
                case ('!', '!' | '%' | None):
                    i_ = i
                case ('%', '!' | '%' | None):
                    i_ = i
    return i_

def _convert_to_int_if_needed(number: int | float) -> int | float:
    number_integer_part = int(number)
    if number == number_integer_part:
        return number_integer_part
    return number

def _get_args_math_function(args_raw: str) -> List[str]:
    args, count, i_ = [], 0, 0
    for i in range(len(args_raw)):
        if args_raw[i] == '(':
            count += 1
        elif args_raw[i] == ')':
            count -= 1
        if args_raw[i] == ',' and count == 0:
            args.append(args_raw[i_:i])
            i_ = i + 1
    args.append(args_raw[i_:])
    return args

def  _string_to_numeric(string: str) -> int | float | None:
    match string:
        case 'pi':
            return math.pi
        case 'e':
            return math.e
        case _:
            if re.search('^-?[0-9]+$', string):
                return int(string)
            elif re.search('^-?[0-9]+\.[0-9]+$', string):
                return float(string)