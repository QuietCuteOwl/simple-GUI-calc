from calculator_UI import MainWidget
from maths_parser import *

class CentralManager:
    def __init__(self) -> None:
        self.widget: MainWidget = MainWidget()
        self.widget.set_button_callback(self.handle_button_press)

    def handle_button_press(self, val: str, current_input: str) -> None:
        if val not in ('AC', 'C', '='):
            self.widget.change_display(change_value= val, join=True)
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
                calculator_core: CalculatorCore = CalculatorCore(self.widget.get_input())
                result: str|None = calculator_core.run(stage=3) # I need to figure out why mypy is giving me this warning and how result could be None
                if result is None:                              # I also need to move all of this out of MyPyPrograms and put in a separate directory
                    return                                      # Then initialize git, pls do it first tomorrow
                self.widget.set_input(val=result, join=False)
                self.widget.update_display()
                print(result)
    def run(self) -> None:
        self.widget.run()

    def clear_all(self):
        self.widget.set_input(val='', join=False)

    def clear_last(self):
        self.widget.set_input(val=self.widget.input_str[:-1], join=False)
        print(f'{self.widget.input_str=}')

def main() -> None:
    manager: CentralManager = CentralManager()
    manager.run()

if __name__ == '__main__':
    main()