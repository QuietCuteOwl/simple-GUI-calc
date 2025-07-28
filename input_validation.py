from utilities import GeneralMethods as gm
import re

# Maybe make preview mode its own function.When special char is pressed (eg: '=') it gets evaluated as "3+2=",check
# if char is a special token, if so then dont concatenate it.Then think of what to add to the calculator, maybe root and log.

class RTEval:
    def __init__(self, manager_methods):
        self.mm = manager_methods
        self.operators = '+-*/^'
    def validate(self, char, expr):
        if len(expr + char) >= 3:
            if self.is_first_value_valid(expr[0]):
                if self.is_last_value_valid(expr=expr + char):
                    if self.is_balanced_parentheses(expr=expr + char):
                        self.evaluate_preview(char=char)
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
                self.mm.add_expr('*')
                return True
            else:
                return True
        elif gm.is_number(char):
            if expr and expr[-1] == ')':
                self.mm.add_expr('*')
                return True
            else:
                return True
        elif char == '.':
            if not self.is_valid_dot(expr=expr):
                return False
            else:
                return True
        elif char in ('AC', 'C'):
            if char == 'AC':
                self.all_clear()
                return True
            else:
                self.clear_last()
                return True
        elif char == '=':
            if not self.is_last_value_valid(expr=expr):
                return False
            else:
                if not self.is_balanced_parentheses(expr=expr):
                    return False
                else:
                    self.evaluate()
                    return True
        else:
            raise Exception(f'Unexpected char: {char}')

    def is_valid_dot(self, expr):
        match = re.search(r'(\d*\.\d*$)', expr)
        if match:
            return False
        else:
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

    def all_clear(self):
        self.mm.all_clear()
        self.mm.request_update_display(self.mm.get_expr())

    def clear_last(self):
        self.mm.pop_input()
        self.mm.request_update_display(self.mm.get_expr())

    def evaluate_preview(self, char):
        result = self.evaluate(preview=True, char=char)
        if result is not None:
            self.mm.request_update_preview_display(value=result)

    def evaluate(self, preview: bool=False, char=None) -> str|None:
        if preview:
            prev_expr = ''
            try:
                prev_expr = self.mm.get_expr() + char
            except TypeError:
                prev_expr = self.mm.get_expr()
            result = self.mm.evaluate(expr=prev_expr, stage=3)
            return result
        else:
            result = self.mm.evaluate(expr=self.mm.get_expr(), stage=3)
            if result is not None:
                self.mm.all_clear()
                self.mm.add_expr(value=result)
                self.mm.request_update_display(self.mm.get_expr())
                return None
            else:
                return None

def main() -> None:

    ...

if __name__ == '__main__':
    main()