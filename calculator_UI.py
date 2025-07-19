import tkinter as tk

from typing import Callable, Optional

class MainWidget:
    def __init__(self) -> None:
        self.root: tk.Tk = tk.Tk()
        self.last_clicked: str = ''
        self.input_str: str = ''
        self.root.title('First time using Tkinter')
        self.entry: tk.Entry = tk.Entry(self.root, width=20, borderwidth=2, font=("Calibri", 18), justify="right")
        self._button_callback: Optional[Callable[[str, str], None]] = None

        window_width: int = 600
        window_height: int = 400

        screen_width: int = self.root.winfo_screenwidth()
        screen_height: int = self.root.winfo_screenheight()

        x: int = (screen_width - window_width) // 2
        y: int = (screen_height - window_height) // 2

        self.root.geometry(f'{window_width}x{window_height}+{x}+{y}')

        self.entry.grid(row=0, column=0, columnspan=4, pady=10, padx=10)

        buttons: list[tuple[str, int, int]|tuple[str, int, int, int]] = [
            ('AC', 1, 0), ('C', 1, 1), ('(', 1, 2), (')', 1, 3),
            ('7', 2, 0), ('8', 2, 1), ('9', 2, 2), ('/', 2, 3),
            ('4', 3, 0), ('5', 3, 1), ('6', 3, 2), ('*', 3, 3),
            ('1', 4, 0), ('2', 4, 1), ('3', 4, 2), ('-', 4, 3),
            ('0', 5, 0), ('.', 5, 1), ('^', 5, 2), ('+', 5, 3),
            ('=', 6, 0, 4),
        ]

        for btn in buttons:
            text: str = btn[0]
            row: int = btn[1]
            column: int = btn[2]
            columnspan: int = btn[3] if len(btn) == 4 else 1
            button: tk.Button = tk.Button(self.root,
                               text=text,
                               width=5 * columnspan + 1,
                               height=2,
                               command=lambda val = text: self.on_click(val))
            button.grid(row=row,
                        column=column,
                        columnspan=columnspan,
                        padx=5,
                        pady=5)

    def set_button_callback(self, callback: Callable[[str, str], None]) -> None:
        self._button_callback = callback

    def get_input(self) -> str:
        return self.input_str

    def set_input(self, val: str, join: bool = False) -> None:
        if not join:
            self.input_str = val
            self.last_clicked = val[-1] if val else ''
            return
        else:
            self.input_str += val
            self.last_clicked = val[-1] if val else ''
            return
    def on_click(self, val: str) -> None:
        self.last_clicked = val
        if val not in ('AC','C', '='):
            self.input_str += val
        if self._button_callback is not None:
            self._button_callback(val, self.input_str)
        return None

    def change_display(self, change_value: str, join: bool =False) -> None:
        if not join:
            self.entry.delete(0, tk.END)
            self.entry.insert(0, change_value)
        else:
            self.entry.insert(tk.END, change_value)

    def update_display(self):
        self.entry.delete(0, tk.END)
        self.entry.insert(0, self.input_str)

    def run(self) -> None:
        self.root.mainloop()

if __name__ == "__main__":
    app: MainWidget = MainWidget()
    app.run()