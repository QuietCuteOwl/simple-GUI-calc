from maths_parser import CalculatorCore
from utilities import GeneralMethods as gm
import re

"""
First figure out how to search for last occurrence of '(' when ')' is pressed,either using regex (which is not implemented
 properly right now) or with a for loop.Then clean the previous code and configure it and other files to take one value at a time
  and create a working example. Dont work on fixing the within parentheses check first as it might take a while.
"""

class RTEval:
    def __init__(self):
        self.buffer = ''
        self.tokens = []
        self.previous = ''
        self.expr = ''
    def validate(self, char):
        if not self.is_first_value_valid():
            ... # show error or remove [0]
        if not self.is_last_value_valid():
            ... # show error
        if not self.is_valid_pair():
            ... # remove second last
        if not self.is_balanced_parentheses():
            ... # show ghost ')' and make up for it in background process or show error
        if not self.is_valid_dot():
            ... # Dont allow the dot
        if not self.allow_closing_parentheses():
            ... # dont allow closing parentheses

    def is_valid_dot(self):
        match = re.search(r'(\d*\.\d*$)', self.expr)
        if match:
            return False
        else:
            return True

    def is_balanced_parentheses(self):
        if self.expr.count('(') == self.expr.count(')'):
            return True
        else:
            return False

    def is_valid_pair(self):
        last = self.expr[-1] if self.expr else None
        second_last = self.expr[-2] if self.expr[-2] else None
        operators = '+-*/^'
        valid_pair = ['*-', '/-', '**']

        if (last is not None and second_last is not None) and (last in operators and second_last in operators) and (last + second_last in valid_pair):
            return True
        else:
            return False
    def is_last_value_valid(self):
        last = self.expr[-1] if self.expr else None
        if last in '+-*/^(' or last is None:
            return False
        else:
            return True

    def is_first_value_valid(self):
        first = self.expr[0] if self.expr else None
        if first in '+-*/^)' and first != '-':
            return False
        else:
            return True

    def allow_closing_parentheses(self):
        is_there_opening_bracket = re.match(r'\($', self.expr)
        if not is_there_opening_bracket:
            return False
        else:
            index = is_there_opening_bracket.end()
            if not self.is_value_inside_parentheses_valid(index):
                return False
            else:
                if self.expr.count('(') < self.expr.count(')'):
                    return False
                else:
                    return True

    def is_value_inside_parentheses_valid(self, index):
        last_index = len(self.expr) - 1
        first = self.expr[index]
        operators = '+-*/^'
        if not index < len(self.expr):
            return False
        if first in operators and first != '-':
            return False
        else:
            return True

    def flash_buffer(self):
        if self.buffer:
            self.tokens.append(self.buffer)
            self.buffer = ''

    def get_current_expr(self):
        tokens = self.tokens.copy()
        if self.buffer:
            tokens.append(self.buffer)
        return tokens

    def clear_all(self):
        self.tokens.clear()
        self.buffer = ''
        self.previous = ''

    def clear_last(self):
        if self.buffer:
            self.buffer = self.buffer[:-1]
        elif self.tokens:
            self.tokens.pop()

def main() -> None:

    ...

if __name__ == '__main__':
    main()