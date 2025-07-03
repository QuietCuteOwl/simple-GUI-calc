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
                    success, var = self.fix_operator_combo()
                    if success:
                        return
                    else:
                        error_tuple = ({sender: f"{sender}"}, {success: f"{success}"}, self.ops_list)
                        print(error_tuple)
        print(f"AT APPENDER: {self.ops_list}")
    def call_to_verify(self, sender):
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
        if len(self.ops_list) == 0:
            return True

        if self.ops_list[-1] == '.':
            return False
        elif self.ops_list[-1].isdigit():
            index = len(self.ops_list) - 1
            for i in range(index, -1, -1):
                if self.ops_list[i] in ['+', '-', '*', '/', '.']:
                    if self.ops_list[i] == '.':
                        pass
                    else:
                        pass

        else:
            return True
    def fix_operator_combo(self):
        print(f"AT F OPS C: {self.ops_list}")
        print(f"{self.ff_list=}")
        if len(self.ff_list) >= 2:  # Checks if last two operators were same
            if self.ops_list[-3] in self.ff_list and self.ops_list[-2] in self.ff_list:
                if self.ops_list[-1] in self.ff_list:
                    self.ops_list.pop()
                    return True, self.ops_list[-1]
            elif self.ops_list[-2] in self.ff_list and self.ops_list[-1] in self.ff_list:
                ops_l = self.ops_list[-1]
                ops_sl = self.ops_list[-2]

            if ops_sl in self.ff_list and ops_l in self.ff_list:
                if ops_sl == '+':
                    if ops_l == '+':
                        self.ops_list.pop()
                        self.ff_list.pop()
                        return True, ops_l
                    elif ops_l == '-':
                        self.ops_list.pop(-2)
                        self.ff_list.pop(-2)
                        return True, ops_sl
                    elif ops_l == '*':
                        self.ops_list.pop(-2)
                        self.ff_list.pop(-2)
                        return True, ops_sl
                    elif ops_l == '/':
                        self.ops_list.pop(-2)
                        self.ff_list.pop(-2)
                        return True, ops_sl
                    else:
                        return False, ops_l
                elif ops_sl == '-':
                    if ops_l == '-':
                        self.ops_list.pop()
                        self.ff_list.pop()
                        return True, ops_l
                    elif ops_l == '+':
                        self.ops_list.pop(-2)
                        self.ff_list.pop(-2)
                        return True, ops_sl
                    elif ops_l == '*':
                        self.ops_list.pop(-2)
                        self.ff_list.pop(-2)
                        return True, ops_sl
                    elif ops_l == '/':
                        self.ops_list.pop(-2)
                        self.ff_list.pop(-2)
                        return True, ops_sl
                    else:
                        return False, ops_l
                elif ops_sl == '*':
                    if ops_l == '*':
                        if self.check_operator_combo(ops_sl, ops_l):
                            return True, ops_sl
                        else:
                            self.collect_count += 1
                            if self.collect_count <= 3:
                                self.fix_operator_combo()
                            else:
                                return False, f"ERROR: {ops_sl=}, {ops_l=}, {self.ops_list[-3]=}"
                    elif ops_l == '+':
                        self.ops_list.pop(-2)
                        self.ff_list.pop(-2)
                        return True, ops_sl
                    elif ops_l == '-':
                        if self.check_operator_combo(ops_sl, ops_l):
                            return True, ops_sl
                        else:
                            self.collect_count += 1
                            if self.collect_count <= 3:
                                self.fix_operator_combo()
                            else:
                                return False, f"ERROR: {ops_sl=}, {ops_l=}, {self.ops_list[-3]=}"
                    elif ops_l == '/':
                        self.ops_list.pop(-2)
                        self.ff_list.pop(-2)
                        return True, ops_sl
                    else:
                        return False, ops_l
                elif ops_sl == '/':
                    if ops_l == '/':
                        self.ops_list.pop()
                        self.ff_list.pop()
                        return True, ops_sl
                    elif ops_l == '+':
                        self.ops_list.pop(-2)
                        self.ff_list.pop(-2)
                        return True, ops_sl
                    elif ops_l == '-':
                        if self.check_operator_combo(ops_sl, ops_l):
                            return True, ops_sl
                        else:
                            self.collect_count += 1
                            if self.collect_count <= 3:
                                self.fix_operator_combo()
                            else:
                                return False, f"ERROR: {ops_sl=}, {ops_l=}, {self.ops_list[-3]=}"
                    elif ops_l == '*':
                        self.ops_list.pop(-2)
                        self.ff_list.pop(-2)
                        return True, ops_sl
                    else:
                        return False, ops_l
        else:
            print(f"{len(self.ff_list)}")

    def check_operator_combo(self, ops_sl, ops_l):
        print(f"AT C OPS C: {self.ops_list}")
        if ops_sl == '*' or '/' and ops_l == '-':
            return True
        elif ops_sl == '-' and ops_l == '*' or '/':
            return True
        elif ops_sl == '*' and ops_l == '*':
            return True
        else:
            return False

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
    def from_eval_symbol(self):
        pass

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
        expression = ''.join(self.ops_list)
        print(f"Display: {expression}")
        print(f"{self.ops_list}")

        self.ans_output.setText("")
        self.ans_output.setText(expression)
        self.__class__.tepm()

    def keyPressEvent(self, event):
        print(f"AT KEYPRESS: {self.ops_list}")
        keys = [46, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 43, 45, 42, 47, 61, 16777219, 16777220, 16777221]
        sender = ''
        if event.key() in keys:
            if event.key() == 46:
                sender = '.'
            elif event.key() == 48:
                sender = '0'
            elif event.key() == 49:
                sender = '1'
            elif event.key() == 50:
                sender = '2'
            elif event.key() == 51:
                sender = '3'
            elif event.key() == 52:
                sender = '4'
            elif event.key() == 53:
                sender = '5'
            elif event.key() == 54:
                sender = '6'
            elif event.key() == 55:
                sender = '7'
            elif event.key() == 56:
                sender = '8'
            elif event.key() == 57:
                sender = '9'
            elif event.key() == 43:
                sender = '+'
            elif event.key() == 45:
                sender = '-'
            elif event.key() == 42:
                sender = '*'
            elif event.key() == 47:
                sender = '/'
            elif event.key() == 61:
                sender = '='
            elif event.key() in [16777220, 16777221]:  # Return or Enter
                sender = '='
            elif event.key() == 16777219:
                self.backspace()



            if sender != '':
                self.verify(sender)

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