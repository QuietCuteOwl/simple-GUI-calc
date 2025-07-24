from calculator_UI import MainWidget
from maths_parser import CalculatorCore
from input_validation import RTEval
from utilities import *

class CentralManager:
    def __init__(self) -> None:
        self.widget: MainWidget = MainWidget()
        self.rte: RTEval = RTEval()
        self.widget.set_button_callback(self.handle_button_press)

    invalid_operator_pair = ('*/', '/*', '+*', '+/', '-*', '-/')

    def handle_button_press(self, val: str, current_input: str) -> None:
        if val in ('AC', 'C', '='):
            self.handle_special_buttons()
        else:
            self.widget.change_display(change_value=val, join=True)
            self.eval_real_time(val=val)
    def calculate_preview(self) -> None:
        expr = ''.join(self.rte.get_current_expr())
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
        self.widget.set_input(val='', join=False)
        self.rte.clear_all()
        return None
    def clear_last(self):
        self.widget.set_input(val=self.widget.input_str[:-1], join=False)
        self.rte.clear_last()
        print(f'{self.widget.input_str=}')

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