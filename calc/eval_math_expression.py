import math
from eval_math_expression_error import *

def _slice_by_index(index, obj):
    return obj[:index], obj[index], obj[index + 1:]

def _find_external_operator(math_expression):
    invalid = _invalid_indexes(math_expression)
    index, count = None, 0
    for i in range(len(math_expression)):
        if math_expression[i] == '(':
            count += 1
        elif math_expression[i] == ')':
            count -= 1
        elif count == 0 and i not in invalid:
            match (math_expression[i], index if index == None else math_expression[index]):
                case ('+', '+' | '-' | '*' | '/' | '^' | '!' | None):
                    index = i
                case ('-', '+' | '-' | '*' | '/' | '^' | '!' | None):
                    index = i
                case ('*', '*' | '/' | '^' | '!' | None):
                    index = i
                case ('/', '*' | '/' | '^' | '!' | None):
                    index = i
                case ('^', '^' | '!' | None):
                    index = i
                case ('!', '!' | None):
                    index = i
    return index

def _invalid_indexes(math_expression):
    invalid_indexes_tuple = tuple()
    for i in range(len(math_expression)):
        if math_expression[i:i+2] in ('*+', '*-', '/+', '/-', '^+', '^-'):
            invalid_indexes_tuple += (i+1,)
        elif math_expression[i:i+2] in ('!+', '!-', '!*', '!/', '!^'):
            invalid_indexes_tuple += (i,)
    return invalid_indexes_tuple

def _get_args(args_str):
    slices, count, i_0 = tuple(), 0, 0
    for i in range(len(args_str)):
        if args_str[i] == '(':
            count += 1
        elif args_str[i] == ')':
            count -= 1
        if args_str[i] == ',' and count == 0:
            slices += (args_str[i_0:i],)
            i_0 = i + 1
    return slices + (args_str[i_0:],)

def check_parentheses(math_expression):
    count = 0
    for i in range(len(math_expression)):
        if math_expression[i] == '(':
            count += 1
        elif math_expression[i] == ')':
            count -= 1
        if count < 0:
            return False
    if count != 0:
        return False
    return True

def eval_math(math_expression: str):
    if math_expression[0] == '(' and math_expression[-1] == ')' and check_parentheses(math_expression[1:-1]):
        return eval_math(math_expression[1:-1])
    try:
        match math_expression:
            case 'pi':
                return math.pi
            case 'e':
                return math.e
            case _:
                return float(math_expression)
    except ValueError:
        
        operator_index = _find_external_operator(math_expression)

        if not operator_index:
            index = math_expression.find('(')
            math_func = math_expression[:index]
            args = _get_args(math_expression[index + 1: -1])
            match math_func:
                # sqrt and abs
                case 'sqrt':
                    return math.sqrt(*map(eval_math, args))
                case 'abs':
                    return math.fabs(*map(eval_math, args))

                # floor and ceil
                case 'floor':
                    return math.floor(*map(eval_math, args))
                case 'ceil':
                    return math.ceil(*map(eval_math, args))

                # degrees and radians
                case 'deg':
                    return math.degrees(*map(eval_math, args))
                case 'rad':
                    return math.radians(*map(eval_math, args))

                # trigonometric functions
                case 'sin':
                    return math.sin(*map(eval_math, args))
                case 'cos':
                    return math.cos(*map(eval_math, args))
                case 'tan':
                    return math.tan(*map(eval_math, args))

                # inverse trigonometric functions
                case 'asin':
                    return math.asin(*map(eval_math, args))
                case 'acos':
                    return math.acos(*map(eval_math, args))
                case 'atan':
                    return math.atan(*map(eval_math, args))

                # hyperbolic functions
                case 'sinh':
                    return math.sinh(*map(eval_math, args))
                case 'cosh':
                    return math.cosh(*map(eval_math, args))
                case 'tanh':
                    return math.tanh(*map(eval_math, args))

                # inverse hyperbolic functions
                case 'asinh':
                    return math.asinh(*map(eval_math, args))
                case 'acosh':
                    return math.acosh(*map(eval_math, args))
                case 'atanh':
                    return math.atanh(*map(eval_math, args))

                # logarithmic functions
                case 'ln':
                    return (lambda x: math.log(x))(*map(eval_math, args))
                case 'log10':
                    return math.log10(*map(eval_math, args))
                case 'log':
                    return (lambda x, y: math.log(x, y))(*map(eval_math, args))
        
        match _slice_by_index(operator_index, math_expression):
            # Exceptions
            case ('', '!', r):
                raise MathExpressionError(f'The mathematical expression is invalid: "!{r}"')
            case (l, '+', ''):
                raise MathExpressionError(f'The mathematical expression is invalid: "{l}+"')
            case (l, '-', ''):
                raise MathExpressionError(f'The mathematical expression is invalid: "{l}-"')

            case (l, '*', ''):
                raise MathExpressionError(f'The mathematical expression is invalid: "{l}*"')
            case ('', '*', r):
                raise MathExpressionError(f'The mathematical expression is invalid: "*{r}"')

            case (l, '/', ''):
                raise MathExpressionError(f'The mathematical expression is invalid: "{l}/"')
            case ('', '/', r):
                raise MathExpressionError(f'The mathematical expression is invalid: "/{r}"')

            case (l, '^', ''):
                raise MathExpressionError(f'The mathematical expression is invalid: "{l}^"')
            case ('', '^', r):
                raise MathExpressionError(f'The mathematical expression is invalid: "^{r}"')

            case (l, '!', ''):
                value = eval_math(l)
                int_value = int(value)
                if value == int_value:
                    return math.factorial(int_value)
                return math.factorial(value)
            case ('', '+', r):
                return eval_math(r)
            case ('', '-', r):
                return -eval_math(r)
            case (l, c, r):
                match c:
                    case '+':
                        return eval_math(l) + eval_math(r)
                    case '-':
                        return eval_math(l) - eval_math(r)
                    case '*':
                        return eval_math(l) * eval_math(r)
                    case '/':
                        return eval_math(l) / eval_math(r)
                    case '^':
                        return eval_math(l) ** eval_math(r)