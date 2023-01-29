import sys
import eval_math_expression
from eval_math_expression_error import *

def main():
    try:
        expression = ''.join(sys.argv[1].split())
    except IndexError:
        sys.exit(0)
    if not expression:
        sys.exit(0)
    elif not eval_math_expression.check_parentheses(expression):
        print('\u001b[33m[*] Some parentheses are missing  [*]\u001b[0m')
        sys.exit(1)
    try:
        result = eval_math_expression.eval_math(expression)
    except MathExpressionError as err:
        print(f'\u001b[31m[!] {err} [!]\u001b[0m')
        sys.exit(1)
    except Exception as err:
        aux = str(str(err).replace('factorial()', 'factorial'))
        print(f'\u001b[31m[!] The mathematical expression is invalid: {aux} [!]\u001b[0m')
        sys.exit(1)
    result_int = int(result)
    if result == result_int:
        print(result_int)
        sys.exit(0)
    print(result)

if __name__ == '__main__':
    main()