from maths_parser import CalculatorCore

class RTEval:
    def __init__(self, expr: str):
        self.calculatorcore: CalculatorCore = CalculatorCore(expr)
    def tokenize(self):
        result = self.calculatorcore.run(1)
        print(result)
    def run(self):
        self.tokenize()

rteval = RTEval('+2')
rteval.run()