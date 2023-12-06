import tkinter as tk
from datetime import datetime

from interface.styling import *


class Logging(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.logging_text = tk.Text(self, width=100, state=tk.DISABLED, bg=BG_COLOR, fg="WHITE",
                                    font=GLOBAL_FONT, highlightthickness=False, bd=0)
        self.logging_text.pack(side=tk.TOP)

    def add_log(self, message: str, missing_parameters=None):
        self.logging_text.configure(state=tk.NORMAL)
        self.logging_text.insert("1.0", message)
        self.logging_text.see(tk.END)

        # Display the log message and missing parameters in a popup
        self.show_popup(message, missing_parameters)

    def show_popup(self, message: str, missing_parameters=None, width=100):
        if missing_parameters is None:
            missing_parameters = []

        max_width = 400

        popup = tk.Toplevel(self.master)  # Use master to reference the root window
        popup.title("Log Message")

        # Prevent resizing
        popup.resizable(False, False)

        label_text = f"Add the following: {message}"

        label_width = min(len(label_text) * 8, max_width)  # Adjust the multiplier as needed
        label = tk.Label(popup, text=label_text, font=GLOBAL_FONT, bg="BLACK", fg="WHITE", width=int(label_width / 8))
        label.pack(padx=3, pady=0)

        close_button = tk.Button(popup, text="Close", command=popup.destroy, font=GLOBAL_FONT,
                                 fg=FG_COLOR, highlightthickness=False, bd=0)
        close_button.pack(pady=0)
