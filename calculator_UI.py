import tkinter as tk
from typing import Callable, Optional

class MainWidget:
    def __init__(self) -> None:
        self.root: tk.Tk = tk.Tk()
        self.last_clicked: str = ''
        self.input_str: str = ''
        self.root.title('First time using Tkinter')
        self.entry: tk.Entry = tk.Entry(self.root, width=30, borderwidth=2, font=("Calibri", 18), justify="right")
        self.preview_entry: tk.Entry = tk.Entry(self.root, width=30, borderwidth=1, font=("Calibri", 18), justify="right", state="readonly")
        self._button_callback: Optional[Callable[[str, str], None]] = None

        window_width: int = 600
        window_height: int = 400

        screen_width: int = self.root.winfo_screenwidth()
        screen_height: int = self.root.winfo_screenheight()

        x: int = (screen_width - window_width) // 2
        y: int = (screen_height - window_height) // 2

        self.root.geometry(f'{window_width}x{window_height}+{x}+{y}')

        self.entry.grid(row=0, column=0, columnspan=4, pady=2, padx=5)
        self.preview_entry.grid(row=1, column=0, columnspan=4)

        buttons: list[tuple[str, int, int]|tuple[str, int, int, int]] = [
            ('AC', 2, 0), ('C', 2, 1), ('(', 2, 2), (')', 2, 3),
            ('7', 3, 0), ('8', 3, 1), ('9', 3, 2), ('/', 3, 3),
            ('4', 4, 0), ('5', 4, 1), ('6', 4, 2), ('*', 4, 3),
            ('1', 5, 0), ('2', 5, 1), ('3', 5, 2), ('-', 5, 3),
            ('0', 6, 0), ('.', 6, 1), ('^', 6, 2), ('+', 6, 3),
            ('=', 7, 0, 4),
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

    def on_click(self, val: str) -> None:
        self.last_clicked = val
        if val not in ('AC','C', '='):
            self.input_str += val
        if self._button_callback is not None:
            self._button_callback(val, self.input_str)
        return None

    def update_display(self, value: str):
        self.entry.delete(0, tk.END)
        self.entry.insert(0, value)

    def update_preview_display(self, value: str) -> None:
        self.preview_entry.config(state="normal")
        self.preview_entry.delete(0, tk.END)
        self.preview_entry.insert(0, value)
        self.preview_entry.config(state="readonly")

    def run(self) -> None:
        self.root.mainloop()

if __name__ == "__main__":
    app: MainWidget = MainWidget()
    app.run()