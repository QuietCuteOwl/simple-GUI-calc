import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit,
                             QPushButton, QHBoxLayout, QVBoxLayout, QGridLayout)
from PyQt5.Qt import Qt

class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.grid = QGridLayout()
        self.buttons = []
        self.arth_buttons = ['+', '-', '×', '÷', '=']
        for num in range(10):
            button = QPushButton(str(num), self)
            button.clicked.connect(self.collect)
            self.buttons.append(button)

            if num == 1:
                self.grid.addWidget(button, 1, 0)
            elif num == 2:
                self.grid.addWidget(button, 1, 1)
            elif num == 3:
                self.grid.addWidget(button, 1, 2)
            elif num == 4:
                self.grid.addWidget(button, 2, 0)
            elif num == 5:
                self.grid.addWidget(button, 2, 1)
            elif num == 6:
                self.grid.addWidget(button, 2, 2)
            elif num == 7:
                self.grid.addWidget(button, 3, 0)
            elif num == 8:
                self.grid.addWidget(button, 3, 1)
            elif num == 9:
                self.grid.addWidget(button, 3, 2)
            elif num == 0:
                self.grid.addWidget(button, 4, 0)

        for sign in self.arth_buttons:
            if sign != "=":
                arth_button = QPushButton(sign, self)
                arth_button.clicked.connect(self.collect)


                if sign == '+':
                    self.grid.addWidget(arth_button, 1, 3)
                elif sign == '-':
                    self.grid.addWidget(arth_button, 2, 3)
                elif sign == '×':
                    self.grid.addWidget(arth_button, 3, 3)
                elif sign == '÷':
                    self.grid.addWidget(arth_button, 4, 3)
            else:
                arth_button = QPushButton(sign, self)
                arth_button.clicked.connect(self.collect)
                self.grid.addWidget(arth_button, 4, 2)


        self.clear_button = QPushButton("C", self)
        self.clear_button.clicked.connect(self.collect)
        self.back_p = QPushButton("⌫", self)
        self.back_p.clicked.connect(self.collect)
        self.decimal = QPushButton(".", self)
        self.decimal.clicked.connect(self.collect)

        self.grid.addWidget(self.clear_button, 1, 4)
        self.grid.addWidget(self.back_p, 2, 4)
        self.grid.addWidget(self.decimal, 4, 1)


        self.ans_output = QLineEdit(self)
        self.grid.addWidget(self.ans_output, 0, 0, 1, 3)

        self.ops_list = []
        self.ff_index = -1
        self.collect_count = 0
        self.ans = ''
        self.fn_list = []
        self.ff_list = []

        self.setLayout(self.grid)
        self.initUI()
    def initUI(self):
        pass

    def collect(self):

        sender = self.sender().text()
        print(f"{sender=}, AT COLLECT: {self.ops_list}")
        self.navigator(sender)
        self.temp_s()

    def navigator(self, sender):

        if sender == 'C':
            self.clear_func()
        elif sender == '⌫':
            self.backspace()
        elif sender in ('×', '÷'):
            self.to_eval_symbols(sender)
        elif sender == '=':
            self.call_to_verify(sender)
        else:
            self.appender(sender)
        print(f"AT NAVIGATOR: {self.ops_list}")
        self.display()
    def appender(self, sender):
        if sender.isdigit():
            self.ops_list.append(sender)
        else:
            if sender == '.':
                if self.handle_decimals():
                    self.ops_list.append(sender)
                else:
                    pass
            else:
                if self.handle_operators():
                    self.ops_list.append(sender)
                    self.ff_list.append(sender)
                else:
                    self.ops_list.append(sender)
                    self.ff_list.append(sender)
                    self.fix_operator_combo()
        print(f"AT APPENDER: {self.ops_list}")
    def call_to_verify(self):
        self.pop_is_equal()

        if self.is_too_short():
            print("Too_Short")
            return
        elif self.is_invalid():
            print("Is_Invalid")
            return
        else:
            self.calculate()
        print(f"AT VERIFY: {self.ops_list}")
    def handle_operators(self):
        print(f"AT H OPS: {self.ops_list}")
        if self.ops_list[-1].isdigit() or self.ops_list[-1] == '.':
            return True
        else:
            return False

    def handle_decimals(self):
        index = len(self.ops_list) - 1
        is_decimal = False

        while index >= 0:
            char = self.ops_list[index]
            if char == '.':
                is_decimal = True
                break
            elif char in ['+', '-', '*', '/']:
                break
            index -= 1

        if is_decimal:
            return False
        else:
            return True
    def fix_operator_combo(self):
        print(f"AT F OPS C: {self.ops_list}")
        print(f"{self.ff_list=}")

        changed = True
        looped = 0
        while changed:
            looped += 1
            print(f"{looped=}")
            changed = False

            if len(self.ff_list) >= 3:  # Checks if last two operators were same
                last_three = self.ops_list[-3:]

                if all(op in self.ff_list for op in last_three):
                    self.ops_list.pop()
                    self.ff_list.pop()
                    changed = True
                    continue

            if len(self.ff_list) >= 2:
                last_two = ''.join(self.ops_list[-2:])

                if self.ops_list[-2] in self.ff_list and self.ops_list[-1] in self.ff_list:

                    if last_two in ['++', '--', '//']:
                        self.ops_list.pop()
                        self.ff_list.pop()
                        changed = True
                        continue

                    if last_two not in ['*-', '/-', '**']:
                        self.ops_list.pop(-2)
                        self.ff_list.pop(-2)
                        changed = True
                        continue

            else:
                print(f"{len(self.ff_list)}")

    def to_eval_symbols(self, sender):
        print(f"AT TES: {self.ops_list}")
        if sender == '×':
            sender = '*'
        elif sender == '÷':
            sender = '/'
        else:
            print(f"GOING TO EVAL: {sender=}")
        self.navigator(sender)
        return

    def pop_is_equal(self):
        print(f"AT POP IE: {self.ops_list}")
        if self.ops_list[-1] == '=':
            self.ops_list.pop()
            self.ff_list.pop()
            return True
        else:
            return False

    def is_too_short(self):
        print(f"AT IS SHORT: {self.ops_list}")
        if len(self.ops_list) <= 2:  # Checks if '=' was pressed without anything else
            return True
        else:
            return False

    def is_invalid(self):
        print(f"AT IS INVALID: {self.ops_list}")
        if self.ops_list[-1] in ['+', '-', '*', '/']:
            return True
        else:
            return False

    def calculate(self):
        print(f"AT CALC: {self.ops_list}")
        expression = ''.join(self.ops_list)
        try:
            self.ans = str(eval(expression))
            print(f"ANS: {self.ans}")
            print(f"ANS TYPE: {type(self.ans)}")

            self.ops_list = []
            for i in self.ans:
                self.ops_list.append(i)

                try:
                    if i.isdigit():
                        self.fn_list.append(i)
                    else:
                        self.ff_list.append(i)
                        self.ff_index += 1
                finally:
                    pass
            self.display()
        except ZeroDivisionError:
            self.clear_func()
            self.ans_output.setText("Zero Division Error")


        # print(self.ops_list)
        # print(self.ops_list)
        # self.collect()
    def clear_func(self):
        print(f"AT C FUNC: {self.ops_list}")
        self.ans_output.clear()
        self.ops_list.clear()
        self.ans = ''
        self.fn_list.clear()
        self.ff_list.clear()
        self.ff_index = -1

    def backspace(self):
        print(f"AT BACK S: {self.ops_list}")
        if len(self.ops_list) < 1:
            return
        else:
            self.ops_list.pop()
            expression = ''.join(self.ops_list)
            self.display()

    def display(self):
        print(f"AT DISPLAY: {self.ops_list}")
        expression = ''.join('×' if x == '*' else
                             '÷' if x == '/' else x
                             for x in self.ops_list)
        print(f"Display: {expression}")
        print(f"{self.ops_list}")

        self.ans_output.setText("")
        self.ans_output.setText(expression)
        self.__class__.tepm()

    def keyPressEvent(self, event):
        print(f"AT KEYPRESS: {self.ops_list}")
        sender = ''
        if event.key() == Qt.Key_Period:
            sender = '.'
        elif event.key() == Qt.Key_0:
            sender = '0'
        elif event.key() == Qt.Key_1:
            sender = '1'
        elif event.key() == Qt.Key_2:
            sender = '2'
        elif event.key() == Qt.Key_3:
            sender = '3'
        elif event.key() == Qt.Key_4:
            sender = '4'
        elif event.key() == Qt.Key_5:
            sender = '5'
        elif event.key() == Qt.Key_6:
            sender = '6'
        elif event.key() == Qt.Key_7:
            sender = '7'
        elif event.key() == Qt.Key_8:
            sender = '8'
        elif event.key() == Qt.Key_9:
            sender = '9'
        elif event.key() == Qt.Key_Plus:
            sender = '+'
        elif event.key() == Qt.Key_Minus:
            sender = '-'
        elif event.key() == Qt.Key_Asterisk:
            sender = '*'
        elif event.key() == Qt.Key_Slash:
            sender = '/'
        elif event.key() == Qt.Key_Equal:
            sender = '='
        elif event.key() == Qt.Key_C:
            sender = 'C'
        elif event.key() in (Qt.Key_Enter, Qt.Key_Return):  # Return or Enter
            sender = '='
        elif event.key() == Qt.Key_Backspace:
            self.backspace()

        if sender != '':
            self.navigator(sender)

    @staticmethod
    def tepm():
        print("________________________________")
    @staticmethod
    def temp_s():
        print("____________")

def main():
    app = QApplication(sys.argv)
    calculator = Calculator()
    calculator.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()