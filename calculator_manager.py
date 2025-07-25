from calculator_UI import MainWidget
from maths_parser import CalculatorCore
from input_validation import RTEval
from utilities import *

class CentralManager:
    def __init__(self) -> None:
        self.widget: MainWidget = MainWidget()
        self.rte: RTEval = RTEval()
        self.widget.set_button_callback(self.handle_button_press)
        self.input_str = ''
        self.expr = ''

    def handle_button_press(self, val: str, current_input: str) -> None:
        print(f'{self.expr=}')
        if val == '=':
            self.evaluate()
            return
        if not self.rte.validate(char=val, expr=self.expr):
            print('Here')
        else:
            self.expr += val
            self.widget.change_display(change_value=val, join=True)
            print(self.expr)
            self.input_str = self.expr
        if not self.widget.get_input() == self.expr:
            print('Out of sync')


    def calculate_preview(self) -> None:
        expr = '7+3'
        calc: CalculatorCore  =CalculatorCore(expr)

        try:
            result = calc.run(stage=3)
            self.widget.change_display(change_value=result, join=False, test=True) # Changing the preview display
        except ZeroDivisionError:
            self.widget.change_display(change_value='/0Err', join=False, test=True)
        except IndexError:
            self.widget.change_display(change_value='...', join=False, test=True)
        except ValueError:
            self.widget.change_display(change_value='"()"...', join=False, test=True)
        except Exception as e:
            print(repr(e))
    def eval_real_time(self, val) -> None:

        self.calculate_preview()
        return None

    def handle_special_buttons(self) -> None:
        last_clicked: str = self.widget.last_clicked
        if not last_clicked in ('AC', 'C', '='):
            return
        else:
            if last_clicked == 'AC':
                self.clear_all()
                self.widget.update_display()
                self.calculate_preview()
                return
            elif last_clicked == 'C':
                self.clear_last()
                self.widget.update_display()
                self.calculate_preview()
                return
            else:
                self.evaluate()
    def run(self) -> None:
        self.widget.run()

    def clear_all(self):
        self.request_set_input(value='', join=False)
        return None
    def clear_last(self):
        self.request_set_input(value=self.widget.input_str[:-1], join=False)
        print(f'{self.widget.input_str=}')

    def evaluate(self) -> None:
        calculator_core: CalculatorCore = CalculatorCore(self.widget.get_input())
        result: str | None = calculator_core.run(stage=3)
        if result is None:
            return
        self.request_set_input(value=result, join=False)
        self.widget.update_display()
        print(result)
        return
    def request_set_input(self, value: str, join=False) -> None:
        self.widget.set_input(val=value, join=join)

def main() -> None:
    manager: CentralManager = CentralManager()
    manager.run()

if __name__ == '__main__':
    main()