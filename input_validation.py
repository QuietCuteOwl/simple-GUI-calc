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

def main() -> None:
    rte: RTEval = RTEval()
    rte.feed(char=5)

if __name__ == '__main__':
    main()