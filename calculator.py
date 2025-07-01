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
        self.first_time = True
        self.ops_list = []
        self.f_index = -1
        self.ff_index = -1
        self.collect_count = 0
        self.ans = ''
        self.fn_list = []
        self.ff_list = []

        self.setLayout(self.grid)
        self.initUI()
    def initUI(self):
        pass

    def collect(self, event):


        # if self.first_time:
        #     print("Connected")
        #     self.first_time = False
        sender = self.sender().text()
        print(f"{sender=} {self.ops_list=}")
        self.temp_s()
        if sender == 'C':
            self.clear_func()
        elif sender == '⌫':
            self.backspace()
        else:
            self.verify(sender)

    def verify(self, sender):
        self.collect_count += 1
        print(f'connect: {self.collect_count}')
        self.temp_s()

        if sender != '=':
            if sender in self.arth_buttons:
                if sender == '×':
                    sender = '*'
                elif sender == '÷':
                    sender = '/'
                else:
                    pass
            else:
                pass
            self.ops_list.append(sender)

            self.f_index += 1
            expression = ''.join(self.ops_list)
            self.fn_list = [i for i in self.ops_list if i.isdigit()]
            self.ff_list = [i for i in self.ops_list if not i.isdigit()]

            if len(self.ff_list) >= 2:  #Checks if last two operators were same
                ops_l = self.ops_list[-1]
                ops_sl = self.ops_list[-2]
                if ops_sl in self.ff_list and ops_l in self.ff_list:
                    if ops_sl == '+':
                        if ops_l == '+':
                            self.ops_list.pop()
                        elif ops_l == '-':
                            self.ops_list.pop(-2)
                        elif ops_l == '*':
                            self.ops_list.pop(-2)
                        elif ops_l == '/':
                            self.ops_list.pop(-2)
                        else:
                            pass
                    elif ops_sl == '-':
                        if ops_l == '-':
                            self.ops_list.pop()
                        elif ops_l == '+':
                            self.ops_list.pop(-2)
                        elif ops_l == '*':
                            self.ops_list.pop(-2)
                        elif ops_l == '/':
                            self.ops_list.pop(-2)
                        else:
                            pass
                    elif ops_sl == '*':
                        if ops_l == '*':
                            pass
                        elif ops_l == '+':
                            self.ops_list.pop(-2)
                        elif ops_l == '-':
                            pass
                        elif ops_l == '/':
                            self.ops_list.pop(-2)
                        else:
                            pass
                    elif ops_sl == '/':
                        if ops_l == '/':
                            self.ops_list.pop()
                        elif ops_l == '+':
                            self.ops_list.pop(-2)
                        elif ops_l == '-':
                            pass
                        elif ops_l == '*':
                            self.ops_list.pop(-2)
                        else:
                            pass
                    elif ops_sl == '.':
                        if ops_l in self.arth_buttons:
                            self.ops_list.pop(-2)

            else:
                print(f"{self.f_index=}")
                self.temp_s()

            self.display(expression)
        else:
            if len(self.ops_list) <= 1: #Checks if '=' was pressed without anything else
                self.ans_output.setText("ERROR:Invalid Expression")
                return
            else:
                ops_l = self.ops_list[-1]
                ops_sl = self.ops_list[-2]

                expression = ''.join(self.ops_list)
                if ops_l == '=':                    #Pops the '='
                    self.ops_list.pop()
                if ops_l in self.ff_list:           #Checks if the operator was right
                    self.ops_list.pop()             #after a number without any number ahead of it
                    expression = ''.join(self.ops_list)
                    self.clear_func()

                    self.calculate(expression)

                else:
                    self.clear_func()
                    self.calculate(expression)
                    print(f"FINAL: {expression}")
                    self.temp_s()

        print(f"LEN: {len(self.ops_list)}")
        print("________________")
    def calculate(self, expression):

        try:
            self.ans = str(eval(expression))

            print(f"ANS: {self.ans}")
            print(f"TYPE: {type(self.ans)}")
            self.temp_s()
            expression = self.ans
            self.display(expression)
            self.ops_list = []
            for i in self.ans:
                self.ops_list.append(i)
                self.f_index += 1
                try:
                    if i.isdigit():
                        self.fn_list.append(i)
                    else:
                        self.ff_list.append(i)
                        self.ff_index += 1
                finally:
                    pass

        except ZeroDivisionError:
            self.clear_func()
            self.ans_output.setText("Zero Division Error")


        # print(self.ops_list)
        # print(self.ops_list)
        # self.collect()
    def clear_func(self):
        self.ans_output.clear()
        self.ops_list.clear()
        self.ans = ''
        self.fn_list.clear()
        self.ff_list.clear()
        self.f_index = -1
        self.ff_index = -1

    def backspace(self):
        if len(self.ops_list) < 1:
            return
        else:
            self.ops_list.pop()
            expression = ''.join(self.ops_list)
            self.display(expression)

    def display(self, expression):
        print(f"Display: {expression}")
        print(f"{self.ops_list}")

        self.ans_output.setText("")
        self.ans_output.setText(expression)
        self.__class__.tepm()

    def keyPressEvent(self, event):
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