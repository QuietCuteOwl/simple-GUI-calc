import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit,
                             QPushButton, QHBoxLayout, QVBoxLayout, QGridLayout)
from PyQt5.Qt import Qt

class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.grid = QGridLayout()
        self.grid.setSpacing(3)
        self.buttons = []
        self.arth_buttons = ['+', '-', '×', '÷', '=']
        for num in range(10):
            button = QPushButton(str(num), self)
            button.setFixedSize(85, 35)
            button.clicked.connect(self.collect)
            self.buttons.append(button)

            if num == 1:
                self.grid.addWidget(button, 2, 0)
            elif num == 2:
                self.grid.addWidget(button, 2, 1)
            elif num == 3:
                self.grid.addWidget(button, 2, 2)
            elif num == 4:
                self.grid.addWidget(button, 3, 0)
            elif num == 5:
                self.grid.addWidget(button, 3, 1)
            elif num == 6:
                self.grid.addWidget(button, 3, 2)
            elif num == 7:
                self.grid.addWidget(button, 4, 0)
            elif num == 8:
                self.grid.addWidget(button, 4, 1)
            elif num == 9:
                self.grid.addWidget(button, 4, 2)
            elif num == 0:
                self.grid.addWidget(button, 5, 0)

        for sign in self.arth_buttons:
            if sign != "=":
                arth_button = QPushButton(sign, self)
                arth_button.setFixedSize(85, 35)
                arth_button.clicked.connect(self.collect)


                if sign == '+':
                    self.grid.addWidget(arth_button, 2, 3)
                elif sign == '-':
                    self.grid.addWidget(arth_button, 3, 3)
                elif sign == '×':
                    self.grid.addWidget(arth_button, 4, 3)
                elif sign == '÷':
                    self.grid.addWidget(arth_button, 5, 3)
            else:
                arth_button = QPushButton(sign, self)
                arth_button.setFixedSize(85, 35)
                arth_button.clicked.connect(self.collect)
                self.grid.addWidget(arth_button, 5, 2)

        self.clear_button = QPushButton("C", self)
        self.clear_button.clicked.connect(self.collect)
        self.back_p = QPushButton("⌫", self)
        self.back_p.clicked.connect(self.collect)
        self.decimal = QPushButton(".", self)
        self.decimal.clicked.connect(self.collect)
        self.parentheses_open = QPushButton("(", self)
        self.parentheses_open.clicked.connect(self.collect)
        self.parentheses_close = QPushButton(")", self)
        self.parentheses_close.clicked.connect(self.collect)

        self.grid.addWidget(self.clear_button, 1, 4)
        self.grid.addWidget(self.back_p, 1, 3)
        self.grid.addWidget(self.decimal, 5, 1)
        self.grid.addWidget(self.parentheses_open, 1, 1)
        self.grid.addWidget(self.parentheses_close, 1, 2)

        self.clear_button.setFixedSize(85, 35)
        self.back_p.setFixedSize(85, 35)
        self.decimal.setFixedSize(85, 35)
        self.parentheses_open.setFixedSize(85, 35)
        self.parentheses_close.setFixedSize(85, 35)

        self.input_and_display = QLineEdit(self)
        self.input_and_display.setMinimumSize(300, 50)
        self.input_and_display.setMaximumSize(700, 100)
        self.grid.addWidget(self.input_and_display, 0, 0, 1, 5)

        self.ops_list = []
        self.ff_index = -1
        self.collect_count = 0
        self.ans = ''
        self.fn_list = []
        self.ff_list = []

        self.setLayout(self.grid)
        self.initUI()
    def initUI(self):

        self.input_and_display.setObjectName("input_and_display")
        self.setStyleSheet("""
            QLineEdit{
                font-size: 50px;
                font-family: calibri;         
            }
            QPushButton{
                border-radius: 14;
                border: 1px solid grey;
            }
        """)

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
            self.call_to_verify()
        else:
            self.appender(sender)
        print(f"AT NAVIGATOR: {self.ops_list}")
        self.display()
    def appender(self, sender):
        if sender.isdigit():
            if len(self.ops_list) > 0  and self.ops_list[-1] == ')':
                self.ops_list.append('*')
            self.ops_list.append(sender)
        else:
            if sender == '.':
                if self.handle_decimals():
                    self.ops_list.append(sender)
                else:
                    pass
            elif sender in ('(', ')'):
                self.manage_parentheses(sender)
            else:
                if self.handle_operators(sender):
                    self.ops_list.append(sender)
                    self.ff_list.append(sender)
                else:
                    if len(self.ops_list) >= 2 and self.ops_list[-2] == '(' or len(self.ops_list) >= 1 and self.ops_list[-1] == '(':
                        print("6/6")
                        pass
                    else:
                        self.ops_list.append(sender)
                        self.ff_list.append(sender)
                        self.sanitize_ops()
        print(f"AT APPENDER: {self.ops_list}")
    def manage_parentheses(self, sender):
        if sender == '(':
            if len(self.ops_list) < 1:
                self.ops_list.append(sender)
                return
            elif self.ops_list[-1].isdigit():
                self.ops_list.append('*')
                self.ops_list.append(sender)
                return
            elif self.ops_list[-1] == ')':
                self.ops_list.append('*')
                self.ops_list.append(sender)
            elif self.ops_list[-1] in ('+', '-', '*', '/'):
                self.ops_list.append(sender)
                return
            elif self.ops_list[-1] == '.':
                pass
                return
            else:
                print(f"{self.ops_list[-1]=}")
                return
        elif sender == ')':
            open_count = self.ops_list.count('(')
            close_count = self.ops_list.count(')')

            if open_count > close_count and self.ops_list and (self.ops_list[-1].isdigit() or self.ops_list[-1] == ')'):
                self.ops_list.append(sender)
                return
            else:
                return
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
    def handle_operators(self, sender):
        print(f"AT H OPS: {self.ops_list}")
        if len(self.ops_list) < 1:

            if sender in ('-', '.'):
                return True
            else:
                return False
        elif self.ops_list[-1].isdigit() or self.ops_list[-1] == '.':
            return True
        elif self.ops_list[-1] == '(':
            if sender == '-':
                print("Reached here")
                return True
            else:
                print("Didnt reach here")
                return False
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
            elif char in ['+', '-', '*', '/', ')']:
                break
            index -= 1

        if is_decimal:
            return False
        else:
            return True
    def sanitize_ops(self):
        print(f"AT SOPS: {self.ops_list}")
        print(f"{self.ff_list=}")

        changed = True
        looped = 0
        while changed:
            looped += 1
            print(f"{looped=}")
            changed = False

            if len(self.ops_list) < 2:
                break

            last_two = self.ops_list[-2:]
            last_three = self.ops_list[-3:] if len(self.ops_list) >= 3 else []

            print(f"LAST TWO: {last_two}")
            print(f"LAST THREE:{last_three}")
            print("2/6")

            if last_three and all(op in self.ff_list for op in last_three):
                self.remove_invalid_combo_last()
                print('3/6')
                changed = True
                continue

            print('4/6')

            if len(last_two) == 2 and all(op in self.ff_list for op in last_two) and not self.is_valid_combo(last_two[0], last_two[1]):
                self.remove_invalid_combo()
                print('5/6')
                changed = True
                continue

        print("6/6")

    def is_valid_combo(self, a, b):

        valid_combo = ('*-', '/-', '**', '(-', ')+', ')-', ')/', ')*')
        return a + b in valid_combo

    def remove_invalid_combo(self, index=-2):
        try:
            print(f"{self.ops_list[index]}{self.ff_list[index]} is popped")
            self.ops_list.pop(index)
            self.ff_list.pop(index)
        except IndexError:
            pass

    def remove_invalid_combo_last(self):

        if self.ops_list:
            print(f'{self.ops_list[-1]} is popped')
            self.ops_list.pop()
        if self.ff_list:
            print(f'{self.ff_list[-1]} is popped')
            self.ff_list.pop()

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
        if len(self.ops_list) < 1:
            return False
        elif self.ops_list[-1] == '=':
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
        if self.ops_list.count('(') != self.ops_list.count(')'):
            self.input_and_display.setText("Unbalanced parentheses")
            return
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
            self.input_and_display.setText("Zero Division Error")
        except (SyntaxError, TypeError, IndexError) as e:
            print(repr(e))


        # print(self.ops_list)
        # print(self.ops_list)
        # self.collect()
    def clear_func(self):
        print(f"AT C FUNC: {self.ops_list}")
        self.input_and_display.clear()
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

        self.input_and_display.setText("")
        self.input_and_display.setText(expression)
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