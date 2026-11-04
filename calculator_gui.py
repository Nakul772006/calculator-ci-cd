"""A polished Tkinter desktop interface for the calculator."""

from collections.abc import Callable
import math
import tkinter as tk

from calculator import add, divide, modulo, multiply, subtract


Operation = Callable[[float, float], float]

COLORS = {
    "background": "#0D1117",
    "surface": "#161B22",
    "display": "#11161D",
    "key": "#21262D",
    "key_hover": "#30363D",
    "utility": "#30363D",
    "utility_hover": "#484F58",
    "operator": "#1F6FEB",
    "operator_hover": "#388BFD",
    "equals": "#238636",
    "equals_hover": "#2EA043",
    "text": "#F0F6FC",
    "muted": "#8B949E",
}

OPERATIONS: dict[str, tuple[str, Operation]] = {
    "+": ("+", add),
    "−": ("−", subtract),
    "×": ("×", multiply),
    "÷": ("÷", divide),
    "mod": ("mod", modulo),
}


class CalculatorApp:
    """Manage the calculator display, keypad, and arithmetic state."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Calculator")
        self.root.configure(bg=COLORS["background"])
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        window_width = min(screen_width, max(480, int(screen_width * 0.65)))
        window_height = min(screen_height, max(600, int(screen_height * 0.8)))
        self.window_height = window_height
        x_position = (screen_width - window_width) // 2
        y_position = (screen_height - window_height) // 2
        root.geometry(
            f"{window_width}x{window_height}+{x_position}+{y_position}"
        )
        root.minsize(min(480, screen_width), min(600, screen_height))
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)

        self.current = "0"
        self.stored_value: float | None = None
        self.pending_operation: tuple[str, Operation] | None = None
        self.last_operation: tuple[str, Operation, float] | None = None
        self.replace_current = True
        self.error = False

        self.expression = tk.StringVar(value="STANDARD")
        self.display = tk.StringVar(value=self.current)

        self._build_interface()
        self._bind_keyboard()
        self.root.focus_set()

    def _build_interface(self) -> None:
        shell = tk.Frame(self.root, bg=COLORS["background"], padx=18, pady=18)
        shell.grid(sticky="nsew")
        shell.grid_rowconfigure(2, weight=1)
        shell.grid_columnconfigure(0, weight=1)

        header = tk.Frame(shell, bg=COLORS["background"])
        header.grid(row=0, column=0, sticky="ew", pady=(0, 14))
        tk.Label(
            header,
            text="CALCULATOR",
            bg=COLORS["background"],
            fg=COLORS["text"],
            font=("TkDefaultFont", 10, "bold"),
        ).pack(side="left")
        tk.Label(
            header,
            text="STANDARD",
            bg=COLORS["background"],
            fg=COLORS["muted"],
            font=("TkDefaultFont", 8, "bold"),
        ).pack(side="right")

        display_panel = tk.Frame(
            shell,
            bg=COLORS["display"],
            padx=16,
            pady=14,
            height=max(140, int(self.window_height * 0.22)),
        )
        display_panel.grid(row=1, column=0, sticky="ew", pady=(0, 14))
        display_panel.grid_propagate(False)
        self.expression_label = tk.Label(
            display_panel,
            textvariable=self.expression,
            anchor="e",
            bg=COLORS["display"],
            fg=COLORS["muted"],
            font=("TkDefaultFont", 10),
        )
        self.expression_label.pack(fill="x", pady=(4, 8))
        self.display_label = tk.Label(
            display_panel,
            textvariable=self.display,
            anchor="e",
            bg=COLORS["display"],
            fg=COLORS["text"],
            font=("TkDefaultFont", 40, "bold"),
        )
        self.display_label.pack(fill="both", expand=True)

        keypad = tk.Frame(shell, bg=COLORS["background"])
        keypad.grid(row=2, column=0, sticky="nsew")
        for column in range(4):
            keypad.grid_columnconfigure(column, weight=1, uniform="key")
        for row in range(5):
            keypad.grid_rowconfigure(row, weight=1, uniform="key")

        keys = (
            (("AC", "clear", "utility"), ("±", "sign", "utility"),
             ("mod", "mod", "utility"), ("÷", "÷", "operator")),
            (("7", "7", "number"), ("8", "8", "number"),
             ("9", "9", "number"), ("×", "×", "operator")),
            (("4", "4", "number"), ("5", "5", "number"),
             ("6", "6", "number"), ("−", "−", "operator")),
            (("1", "1", "number"), ("2", "2", "number"),
             ("3", "3", "number"), ("+", "+", "operator")),
            (("DEL", "delete", "utility"), ("0", "0", "number"),
             (".", ".", "number"), ("=", "equals", "equals")),
        )

        for row, key_row in enumerate(keys):
            for column, (label, action, style) in enumerate(key_row):
                self._create_key(keypad, label, action, style, row, column)

    def _create_key(
        self,
        parent: tk.Frame,
        label: str,
        action: str,
        style: str,
        row: int,
        column: int,
    ) -> None:
        color_key = "key" if style == "number" else style
        hover_key = {
            "number": "key_hover",
            "utility": "utility_hover",
            "operator": "operator_hover",
            "equals": "equals_hover",
        }[style]
        button = tk.Button(
            parent,
            text=label,
            command=lambda: self._activate(action),
            bg=COLORS[color_key],
            fg=COLORS["text"],
            activebackground=COLORS[hover_key],
            activeforeground=COLORS["text"],
            relief="flat",
            borderwidth=0,
            highlightthickness=0,
            cursor="hand2",
            font=("TkDefaultFont", 15 if len(label) < 3 else 10, "bold"),
            takefocus=False,
        )
        button.grid(row=row, column=column, sticky="nsew", padx=4, pady=4, ipadx=4, ipady=9)
        button.bind("<Enter>", lambda _event: button.configure(bg=COLORS[hover_key]))
        button.bind("<Leave>", lambda _event: button.configure(bg=COLORS[color_key]))

    def _bind_keyboard(self) -> None:
        self.root.bind("<Key>", self._on_key)
        self.root.bind("<Return>", lambda _event: self._activate("equals"))
        self.root.bind("<KP_Enter>", lambda _event: self._activate("equals"))
        self.root.bind("<BackSpace>", lambda _event: self._activate("delete"))
        self.root.bind("<Escape>", lambda _event: self._activate("clear"))

    def _on_key(self, event: tk.Event) -> str | None:
        if event.char in "0123456789." and event.char:
            self._activate(event.char)
        elif event.char in "+-*/%":
            action = {
                "-": "−",
                "*": "×",
                "/": "÷",
                "%": "mod",
            }.get(event.char, event.char)
            self._activate(action)
        elif event.char == "=":
            self._activate("equals")
        else:
            return None
        return "break"

    def _activate(self, action: str) -> None:
        if action.isdigit() or action == ".":
            self._input_digit(action)
        elif action == "clear":
            self._clear()
        elif action == "delete":
            self._delete_digit()
        elif action == "sign":
            self._toggle_sign()
        elif action == "equals":
            self._equals()
        elif action in OPERATIONS:
            self._choose_operation(action)

    def _input_digit(self, digit: str) -> None:
        if self.error or self.replace_current:
            self.current = "0." if digit == "." else digit
            self.replace_current = False
            self.error = False
            self.expression.set("STANDARD")
        elif digit == ".":
            if "." not in self.current:
                self.current += "."
        elif len(self.current.replace("-", "").replace(".", "")) < 15:
            self.current = digit if self.current == "0" else self.current + digit
        self._refresh_display()

    def _choose_operation(self, symbol: str) -> None:
        if self.error:
            return
        operation = OPERATIONS[symbol]
        if self.pending_operation and not self.replace_current:
            if not self._calculate_pending():
                return
        else:
            self.stored_value = float(self.current)

        self.pending_operation = operation
        self.last_operation = None
        self.expression.set(f"{self._format(self.stored_value)} {symbol}")
        self.replace_current = True

    def _equals(self) -> None:
        if self.error:
            return
        if self.pending_operation is not None:
            symbol, operation = self.pending_operation
            second = float(self.current)
            first = self.stored_value
            if first is None:
                return
            self.expression.set(
                f"{self._format(first)} {symbol} {self._format(second)} ="
            )
            try:
                value = operation(first, second)
                self.current = self._format_result(value)
            except (ZeroDivisionError, OverflowError):
                self._show_error("Cannot divide by zero" if second == 0 else "Result out of range")
                return
            self.last_operation = (symbol, operation, second)
            self.pending_operation = None
            self.stored_value = None
            self.replace_current = True
        elif self.last_operation is not None:
            symbol, operation, second = self.last_operation
            first = float(self.current)
            self.expression.set(
                f"{self._format(first)} {symbol} {self._format(second)} ="
            )
            try:
                self.current = self._format_result(operation(first, second))
            except (ZeroDivisionError, OverflowError):
                self._show_error("Cannot divide by zero" if second == 0 else "Result out of range")
                return
            self.replace_current = True
        self._refresh_display()

    def _calculate_pending(self) -> bool:
        if self.pending_operation is None or self.stored_value is None:
            return False
        _symbol, operation = self.pending_operation
        second = float(self.current)
        try:
            value = operation(self.stored_value, second)
            self.current = self._format_result(value)
        except (ZeroDivisionError, OverflowError):
            self._show_error("Cannot divide by zero" if second == 0 else "Result out of range")
            return False
        self.stored_value = float(self.current)
        self._refresh_display()
        return True

    def _clear(self) -> None:
        self.current = "0"
        self.stored_value = None
        self.pending_operation = None
        self.last_operation = None
        self.replace_current = True
        self.error = False
        self.expression.set("STANDARD")
        self._refresh_display()

    def _delete_digit(self) -> None:
        if self.error:
            self._clear()
            return
        if self.replace_current:
            return
        self.current = self.current[:-1]
        if self.current in ("", "-"):
            self.current = "0"
        self._refresh_display()

    def _toggle_sign(self) -> None:
        if self.error:
            self._clear()
        elif float(self.current) != 0:
            self.current = self.current[1:] if self.current.startswith("-") else "-" + self.current
            self.replace_current = False
            self._refresh_display()

    def _show_error(self, message: str) -> None:
        self.current = "Error"
        self.stored_value = None
        self.pending_operation = None
        self.last_operation = None
        self.replace_current = True
        self.error = True
        self.expression.set(message)
        self._refresh_display()

    @staticmethod
    def _format(value: float | None) -> str:
        return "0" if value is None else format(value, ".12g")

    @classmethod
    def _format_result(cls, value: float) -> str:
        if not math.isfinite(value):
            raise OverflowError("Calculator result is not finite.")
        return cls._format(value)

    def _refresh_display(self) -> None:
        self.display.set(self.current)
        font_size = max(18, 34 - max(0, len(self.current) - 9) * 2)
        self.display_label.configure(font=("TkDefaultFont", font_size, "bold"))


def main() -> None:
    """Launch the desktop calculator."""
    root = tk.Tk()
    CalculatorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
