from maths_parser import CalculatorCore
from utilities import GeneralMethods

class RTEval:
    def __init__(self):
        self.buffer = ''
        self.tokens = []
        self.previous = ''
    def feed(self, char):
        if GeneralMethods.is_number(char) or char == '.':
            self.buffer += char
        elif char in '+-*/^':
            self.flash_buffer()
            self.tokens.append(char)
        elif char in '()':
            self.flash_buffer()
            self.tokens.append(char)
        else:
            pass
        self.previous = char

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
    rte: RTEval = RTEval()
    rte.feed(char='5')
    rte.flash_buffer()
    print(rte.tokens)

if __name__ == '__main__':
    main()