from calculator_UI import MainWidget
from maths_parser import *
from input_validation import *
from utilities import *

class CentralManager:
    def __init__(self) -> None:
        self.widget: MainWidget = MainWidget()
        self.widget.set_button_callback(self.handle_button_press)

    invalid_operator_pair = ('*/', '/*', '+*', '+/', '-*', '-/')

    def handle_button_press(self, val: str, current_input: str) -> None:
        if val not in ('AC', 'C', '='):
            self.widget.change_display(change_value= val, join=True)
            if val in ('+', '-', '*', '/'):
                second_last: str|None = self.widget.input_str[-2] if GeneralMethods.it_exists(var=self.widget.input_str, index=-2) else None
                if second_last in ('+', '-', '*', '/'):
                    self.manage_operator_conflict(second_last)
                    return None
                else:
                    pass
            return None
        else:
            self.handle_special_buttons()
            return None
    def handle_special_buttons(self) -> None:
        last_clicked: str = self.widget.last_clicked
        if not last_clicked in ('AC', 'C', '='):
            return
        else:
            if last_clicked == 'AC':
                self.clear_all()
                self.widget.update_display()
            elif last_clicked == 'C':
                self.clear_last()
                self.widget.update_display()
            else:
                self.evaluate()
    def run(self) -> None:
        self.widget.run()

    def clear_all(self):
        self.widget.set_input(val='', join=False)

    def clear_last(self):
        self.widget.set_input(val=self.widget.input_str[:-1], join=False)
        print(f'{self.widget.input_str=}')

    def manage_operator_conflict(self, second_last: str) -> None:
        ...

    def evaluate(self) -> None:
        calculator_core: CalculatorCore = CalculatorCore(self.widget.get_input())
        result: str | None = calculator_core.run(stage=3)
        if result is None:
            return
        self.widget.set_input(val=result, join=False)
        self.widget.update_display()
        print(result)
        return

def main() -> None:
    manager: CentralManager = CentralManager()
    manager.run()

if __name__ == '__main__':
    main()