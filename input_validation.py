from maths_parser import CalculatorCore
from utilities import GeneralMethods

class RTEval:
    def __init__(self, expr: str):
        self.expr = expr
        self.calculatorcore: CalculatorCore = CalculatorCore(self.expr)
        self.buffer = ''
    def tokenize(self):
        result = self.calculatorcore.run(1)
        print(result)
    def process_buffer_tokens(self):
        self.buffer += self.expr[0] if self.expr else None
        if GeneralMethods.is_number(self.buffer):
            return
        else:
            if self.buffer in ('+', '-', '*', '/'):
                ...

    def run(self):
        self.tokenize()

rteval = RTEval('+2')
rteval.run()