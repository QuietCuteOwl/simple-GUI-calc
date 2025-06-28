import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit,
                             QPushButton, QHBoxLayout, QVBoxLayout)
from PyQt5.Qt import Qt
from unicodedata import digit




class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.vbox1 = QVBoxLayout()
        self.vbox2 = QVBoxLayout()
        self.vbox3 = QVBoxLayout()
        self.vbox4 = QVBoxLayout()
        self.vbox5 = QVBoxLayout()
        self.buttons = []
        self.ops_buttons = []
        self.arth_buttons = ['+', '-', '×', '÷', '=']
        for num in range(10):
            button = QPushButton(str(num), self)
            button.clicked.connect(self.collect)
            self.buttons.append(button)

            if num in [1, 4, 7]:
                self.vbox1.addWidget(button)
            elif num in [2, 5, 8]:
                self.vbox2.addWidget(button)
            elif num in [3, 6, 9]:
                self.vbox3.addWidget(button)
            elif num == 0:
                self.vbox4.addWidget(button)
        for sign in self.arth_buttons:
            if sign != "=":
                arth_button = QPushButton(sign, self)
                arth_button.clicked.connect(self.collect)
                self.ops_buttons.append(arth_button)
                self.vbox5.addWidget(arth_button)
            else:
                arth_button = QPushButton(sign, self)
                arth_button.clicked.connect(self.collect)
                self.ops_buttons.append(arth_button)
                self.vbox4.addWidget(arth_button)
        self.clear_button = QPushButton("C", self)
        self.clear_button.clicked.connect(self.collect)
        self.back_p = QPushButton("⌫", self)
        self.back_p.clicked.connect(self.backspace)
        self.decimal = QPushButton(".", self)
        self.decimal.clicked.connect(self.collect)
        self.vbox3.addWidget(self.decimal)
        self.vbox4.addWidget(self.back_p)
        self.vbox4.addWidget(self.clear_button)
        self.ans_output = QLineEdit(self)
        self.first_time = True
        self.ops_list = []
        self.f_index = -1
        self.ff_index = -1
        self.collect_count = 0
        self.ans = ''
        self.fn_list = []
        self.ff_list = []
        self.initUI()
    def initUI(self):

        # for button in self.buttons:
        #     button_name = int(button.text())
        #     print(button_name)


        vbox6 = QVBoxLayout()

        vbox6.addWidget(self.ans_output)



        hbox7 = QHBoxLayout()


        hbox7.addLayout(self.vbox1)
        hbox7.addLayout(self.vbox2)
        hbox7.addLayout(self.vbox3)
        hbox7.addLayout(self.vbox4)
        hbox7.addLayout(self.vbox5)

        vbox7 = QVBoxLayout()

        vbox7.addLayout(vbox6)
        vbox7.addLayout(hbox7)

        self.setLayout(vbox7)



    def collect(self, event):
        # if self.first_time:
        #     print("Connected")
        #     self.first_time = False
        sender = self.sender().text()
        print(f"{sender=} {self.ops_list=}")

        if sender == 'C':
            self.clear_func()
        else:
            self.verify(sender)

    def verify(self, sender):
        print(f"LST_T: {self.ops_list}")
        self.collect_count += 1
        print(f'connect: {self.collect_count}')
        if sender != '=':
            self.ops_list.append(sender)
            self.f_index += 1
            expression = ''.join(self.ops_list)
            f_list = self.ops_list
            self.fn_list = [i for i in f_list if i.isdigit()]
            self.ff_list = [i for i in f_list if not i.isdigit()]

            if len(self.ff_list) >= 2:
                if self.ff_list[-1] == self.ff_list[-2]:
                    print(self.ff_list[-1])
                    self.ops_list.pop()
                    print("You cannot do the same operation twice")
                    print(f"IDX: {self.f_index}")
            else:
                print(f"IDX: {self.f_index}")
            print(f"LST: {self.ops_list}")
            self.display(expression)
            print(f"VRY_I: {expression}")
        else:
            print(self.ops_list)
            if len(self.ops_list) <= 0:
                self.ans_output.setText("Invalid")
                return
            else:
                expression = ''.join(self.ops_list)
                if self.ops_list and self.ops_list[-1] == '=':
                    self.ops_list.pop()
                if self.ops_list and self.ops_list[-1] in self.ff_list:
                    self.clear_func()
                    self.ans_output.setText("Error:Operator right after number")
                else:
                    expression = expression.replace('×', '*').replace('÷', '/')
                    self.ff_list = []
                    self.fn_list = []
                    self.f_index = -1
                    self.ff_index = -1
                    self.calculate(expression)
                    print(f"VRY_E: {expression}")
        print(len(self.ops_list))
    def calculate(self, expression):

        try:
            self.ans = str(eval(expression))
            print(f"ANS: {self.ans}")
            print(f"TYPE: {type(self.ans)}")
            expression = self.ans
            self.display(expression)
            print(f"CALC:{expression}")
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
        self.f_index = 0
        self.ff_index = -1
        print(f"CLR2: {self.ops_list}")

    def backspace(self):
        if len(self.ops_list) < 1:
            return
        else:
            self.ops_list.pop()
            expression = ''.join(self.ops_list)
            self.display(expression)

    def display(self, expression):
        print(f"Display: {expression}")


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
        else:
            print(event.text())
            print(event.key())

    @staticmethod
    def tepm():
        print("________________________________")
if __name__ == '__main__':
    app = QApplication(sys.argv)
    calculator = Calculator()
    calculator.show()
    sys.exit(app.exec_())