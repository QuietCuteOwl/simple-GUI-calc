import re
from decimal import Decimal
from typing import Union
from utilities import GeneralMethods


class Tokenizer:
    def __init__(self, expr):
        self.expr = expr
        self.caret = 0

    NUMBER = 'NUMBER'
    ADDITION = '+'
    SUBTRACTION = '-'
    MULTIPLICATION = '*'
    DIVISION = '/'
    EXPONENTIATION = '^'
    PARENTHESES_LEFT = '('
    PARENTHESES_RIGHT = ')'

    TokenSpecification = [
        (re.compile(r'^\s+'), None),
        (re.compile(r'^(?:\d+(?:\.\d*)?|(?:\.\d+))'), NUMBER),
        (re.compile(r'^\+'), ADDITION),
        (re.compile(r'^\-'), SUBTRACTION),
        (re.compile(r'^\*'), MULTIPLICATION),
        (re.compile(r'^\/'), DIVISION),
        (re.compile(r'^\^'), EXPONENTIATION),
        (re.compile(r'^\('), PARENTHESES_LEFT),
        (re.compile(r'^\)'), PARENTHESES_RIGHT),
    ]

    def match_token(self, regex, expr_slice):
        matched = regex.match(expr_slice)
        if matched is None:
            return None

        self.caret += len(matched.group(0))
        return matched.group(0)

    def has_more_token(self):
        return self.caret < len(self.expr)

    def get_next_token(self):
        if not self.has_more_token():
            return None

        expr_slice = self.expr[self.caret:]

        for regex, token_type in self.TokenSpecification:
            token_value = self.match_token(regex, expr_slice)

            if token_value is None:
                continue

            if token_type is None:
                return self.get_next_token()

            return {
                'type': token_type,
                'value': token_value,
            }
        raise Exception(f'Unexpected Token: {expr_slice[0]}')


class ToRPN:
    def __init__(self, tokenized_expr):
        self.tokenized_expr = tokenized_expr

    operators = {
        '+': {'prec': 1, 'assoc': 'left'},
        '-': {'prec': 1, 'assoc': 'left'},
        '*': {'prec': 2, 'assoc': 'left'},
        '/': {'prec': 2, 'assoc': 'left'},
        '^': {'prec': 3, 'assoc': 'right'},
        'neg': {'prec': 3, 'assoc': 'right'},
    }

    def to_rpn(self):
        stack = []
        output = []
        op_symbol = list(self.operators.keys())
        for token in self.tokenized_expr:
            if GeneralMethods.is_number(x=token):
                output.append(token)
                continue
            elif token in op_symbol:
                while (
                        stack and
                        stack[-1] in self.operators and
                        stack != '('
                ):
                    o2 = stack[-1]
                    p1 = self.operators[token]['prec']
                    a1 = self.operators[token]['assoc']
                    p2 = self.operators[o2]['prec']

                    if (p2 > p1) or ((p2 == p1) and (a1 == 'left')):
                        output.append(stack.pop())
                    else:
                        break
                stack.append(token)

            elif token == '(':
                stack.append(token)
            elif token == ')':
                while stack:
                    top = stack.pop()
                    if top == '(':
                        break
                    output.append(top)
                else:
                    raise ValueError('Mismatched Parentheses')

        while stack:
            output.append(stack.pop())

        return output

class Calculate:
    def __init__(self, expr_rpn):
        self.expr_rpn = expr_rpn
    def calculate(self) -> str|float|None:

        output = []

        for token in self.expr_rpn:
            if GeneralMethods.is_number(x=token):
                output.append(Decimal(token))
                continue
            else:
                if token == 'neg':
                    value = Decimal(output.pop())
                    output.append(-value)
                    continue
                try:
                    right = Decimal(output.pop())
                    left = Decimal(output.pop())
                except IndexError:
                    raise IndexError
                if token == '+':
                    output.append(left + right)
                    continue
                elif token == '-':
                    output.append(left - right)
                    continue
                elif token == '*':
                    output.append(left * right)
                    continue
                elif token == '/':
                    if right == 0:
                        if left == 0:
                            raise ZeroDivisionError('Division by zero')
                        else:
                            possible_infinity = float('inf')
                            return possible_infinity
                    output.append(left / right)
                    continue
                elif token == '^':
                    output.append(left ** right)
                    continue
                else:
                    raise Exception(f'Invalid Token: {token}')
        answer: str|None = str(output[0]) if output else None
        return answer

class CalculatorCore:

    def run(self, expr: str, stage: int) -> Union[None, list[str]]:
        if not (1 <= stage <= 3):
            return None
        else:
            tokenized = self.tokenize(expr)
            match stage:
                case 1:
                    return tokenized
                case 2:
                    return self.rpn_converter(tokenized)
                case 3:
                    return self.evaluate(self.rpn_converter(tokenized))
                case _:
                    return None

    def tokenize(self, expr) -> list[str]:
        tokenizer: Tokenizer = Tokenizer(expr=expr)
        tokens: list[str] = []
        previous_token: None|str = None
        help_unary: bool = False

        while tokenizer.has_more_token():
            token: dict[str, str] = tokenizer.get_next_token()
            if help_unary:
                tokens.append('neg')
                help_unary = False
            if token is not None:
                if ((token['value'] == '-') and
                    ((previous_token is None) or (previous_token == '(') or (previous_token in ToRPN.operators))):
                    previous_token = token['value']
                    help_unary = True
                    continue
                tokens.append(token['value'])
                previous_token = token['value']

        return tokens

    def rpn_converter(self, tokenized_expr):
        return ToRPN(tokenized_expr).to_rpn()

    def evaluate(self, rpn_expr):
        return Calculate(rpn_expr).calculate()

def main():
    print('Running file directly')
    casl = CalculatorCore()
    print(casl.run(expr='3.1.4', stage=1))

if __name__ == '__main__':
    main()
