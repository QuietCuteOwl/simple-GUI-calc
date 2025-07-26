from calculator_UI import MainWidget
from maths_parser import CalculatorCore
from input_validation import RTEval
from utilities import ManagerMethods


class CentralManager:
    def __init__(self) -> None:
        self.widget: MainWidget = MainWidget()
        self.rte: RTEval = RTEval()
        self.widget.set_button_callback(self.handle_button_press)
        self.expr: str = ''
    def handle_button_press(self, val: str, current_input: str) -> None:
        print(f'{self.expr=}')

        if not self.rte.validate(char=val, expr=self.expr):
            print('Here')
        else:
            self.expr += val
            self.widget.change_display(change_value=val, join=True)
            print(self.expr)

    def run(self) -> None:
        self.widget.run()

    def pop_input(self, pop: int = -1) -> str:
        if not self.expr:
            return self.expr
        else:
            try:
                expr_list: list[str] = list(self.expr)
                expr_list.pop(pop)
                self.expr = ''.join(expr_list)
            except IndexError:
                raise IndexError
            return self.expr

    def get_expr(self):
        return self.expr

    def all_clear(self):
        self.expr = ''

    def add_expr(self, value: str):
        self.expr += value

    def request_update_display(self, value: str):
        self.widget.update_display(value=value)

    def evaluate(self, stage: int):
        evaluator: CalculatorCore = CalculatorCore()
        try:
            evaluator.run(expr=self.expr, stage=stage)
        except ValueError:
            return f'Mismatched Parentheses'
        except IndexError:
            return f'Invalid Input'
        except ZeroDivisionError:
            return f'Division by Zero'
        except Exception as e:
            print(repr(e))
            return e

def main() -> None:
    manager: CentralManager = CentralManager()
    evaluator: CalculatorCore = CalculatorCore()
    manager_methods: ManagerMethods = ManagerMethods(manager_instance=manager, evaluator_instance=evaluator)

    manager.run()

if __name__ == '__main__':
    main()