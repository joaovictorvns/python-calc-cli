import sys

from eval_math import eval_math, EvalMathExpressionError

def main(math_expression):
    print(eval_math(math_expression))

if __name__ == '__main__':
    main(sys.argv[1])