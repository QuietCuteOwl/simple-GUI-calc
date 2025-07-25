from maths_parser import CalculatorCore
from utilities import GeneralMethods as gm
import re

# To-Do Tomorrow: Make a method in manager to change/edit expr str from another file then implement automatic addition of '*'
# when an opening parentheses is after a number and a closing is after a number.Define new or update existing methods for
# all_clear and clear_last then clean the manager file if necessary.Make a method for calculating when user presses '='.

class RTEval:
    def __init__(self):
        self.operators = '+-*/^'
    def validate(self, char, expr):
        if char in self.operators + ')':
            if len(expr) == 0:
                if not self.is_first_value_valid(char=char):
                    return False
                else:
                    return True
            else:
                if char in self.operators:
                    if not self.is_valid_pair(char=char, expr=expr):
                        return False
                    else:
                        return True
                else:
                    if char == ')':
                        if not self.allow_closing_parentheses(expr=expr):
                            return False
                        else:
                            return True
                    else:
                        return False
        elif char == '(':
            if expr and (gm.is_number(expr[-1]) or expr[-1] == ')'):
                expr += '*'
                return True
            else:
                return True
        elif gm.is_number(char):
            if expr and expr[-1] == ')':
                expr += '*'
                return True
            else:
                return True
        elif char == '.':
            if not self.is_valid_dot(expr=expr):
                return False
            else:
                print('Hey')
                return True
        elif char in ('AC', 'C'):
            if char == 'AC':
                ... # clear all
            else:
                ... # clear last
        elif char == '=':
            if not self.is_last_value_valid(expr=expr):
                return False
            else:
                if not self.is_balanced_parentheses(expr=expr):
                    return False
                else:
                    return True
        else:
            raise Exception(f'Unexpected char: {char}')

    def is_valid_dot(self, expr):
        match = re.search(r'(\d*\.\d*$)', expr)
        if match:
            return False
        else:
            print('Hi')
            return True

    def is_balanced_parentheses(self, expr):
        if expr.count('(') == expr.count(')'):
            return True
        else:
            return False

    def is_valid_pair(self, char, expr):
        last = char
        second_last = expr[-1] if expr else None
        operators = '+-*/^'
        valid_pair = ['*-', '/-', '**', '(-']

        if second_last is None:
            if not self.is_first_value_valid(char=char):
                return False
            else:
                return True
        elif not second_last in operators:
            return True # needs refining for parentheses later, possibly splitting into another method
        elif second_last + last in valid_pair:
            return True
        else:
            return False
    def is_last_value_valid(self, expr):
        last = expr[-1] if expr else None
        if last is None or last in '+-*/^(':
            return False
        else:
            return True

    def is_first_value_valid(self, char):
        if char in '+-*/^)' and char != '-':
            return False
        else:
            return True

    def allow_closing_parentheses(self, expr):
        for i in range(len(expr) - 1, -1, -1):   # checks if a opening parentheses exist,if not then false
            if expr[i] == '(':
                break
        else:
            return False
        if expr.count('(') <= expr.count(')'):   # checks if there are less or equal opening brackets than closing ones.
            return False
        elif expr and expr[-1] in '-+*/^(':   # if the last value before closing is an operator or an opening parentheses then false
            return False
        else:
            return True

    def is_value_inside_parentheses_valid(self, index, expr):
        last_index = len(expr) - 1
        first = expr[index]
        operators = '+-*/^'
        if not index < len(expr):
            return False
        if first in operators and first != '-':
            return False
        else:
            return True


def main() -> None:

    ...

if __name__ == '__main__':
    main()