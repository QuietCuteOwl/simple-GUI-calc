from calculator_UI import MainWidget
from maths_parser import CalculatorCore
from input_validation import RTEval
from utilities import ManagerMethods

class CentralManager:
    def __init__(self) -> None:
        self.widget: MainWidget = MainWidget()
        self.expr: str = ''
        self.evaluator: CalculatorCore = CalculatorCore()
        self.manager_methods: ManagerMethods = ManagerMethods(manager_instance=self, evaluator_instance=self.evaluator)
        self.rte: RTEval = RTEval(manager_methods=self.manager_methods)
        self.widget.set_button_callback(self.handle_button_press)

    def handle_button_press(self, val: str, current_input: str) -> None:
        print(f'{self.expr=}')

        if not self.rte.validate(char=val, expr=self.expr):
            print('Here')
        else:
            if not self.is_special_char(val=val):
                self.expr += val
                self.widget.update_display(value=self.expr)
            print(self.expr)

    def is_special_char(self, val: str):
        if val in ('AC', 'C', '='):
            return True
        else:
            return False

    def get_expr(self):
        return self.expr

    def run(self) -> None:
        self.widget.run()

def main() -> None:
    manager: CentralManager = CentralManager()
    manager.run()

if __name__ == '__main__':
    main()