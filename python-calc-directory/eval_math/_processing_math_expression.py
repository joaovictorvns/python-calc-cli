from typing import List
import re

def _remove_spaces(string: str) -> str:
    return re.sub('\s+', '', string)

def _remove_redundant_operators(string: str) -> str:
    while True:
        match_ = re.search('[+-][+-]+', string)
        if not match_:
            break
        if match_.group().count('-')%2 == 0:
            string = string.replace(match_.group(), '+')
        else:
            string = string.replace(match_.group(), '-')
    return string

def _remove_plus_sign(math_expression: str) -> str:
    math_expression = math_expression.replace('*+', '*').replace('/+', '/').replace('^+', '^+').replace('(+', '(')
    if math_expression[0] == '+':
        return math_expression[1:]
    return math_expression