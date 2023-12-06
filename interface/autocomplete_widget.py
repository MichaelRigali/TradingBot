import tkinter as tk
import typing

class Autocomplete(tk.Entry):
    def __init__(self, symbols: typing.List[str], *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._symbols = symbols

        self._lb: tk.Listbox = None
        self._lb_open = False

        self.bind("<Up>", self._up_down)
        self.bind("<Down>", self._up_down)
        self.bind("<Right>", self._select)
        self.bind("<Button-1>", self._select_left_click)

        self._var = tk.StringVar()
        self.configure(textvariable=self._var)
        self._var.trace("w", self._changed)

    def _changed(self, var_name: str, index: str, mode: str):
        self._var.set(self._var.get().upper())

        if self._var.get() == "":
            if self._lb_open:
                self._lb.destroy()
                self._lb_open = False
        elif not self._lb_open:
            self._lb = tk.Listbox(height=8)
            self._lb.place(x=self.winfo_x() + 2, y=self.winfo_y() + self.winfo_height() + 4)
            self._lb_open = True

            # Bind the ListboxSelect event to handle both arrow key selection and left-click
            self._lb.bind("<<ListboxSelect>>", self._listbox_select)

        symbols_matched = [symbol for symbol in self._symbols if symbol.startswith(self._var.get())]

        if self._lb_open:
            try:
                self._lb.delete(0, tk.END)
            except tk.TclError:
                pass

            for symbol in symbols_matched:
                self._lb.insert(tk.END, symbol)

    def _select(self, event: tk.Event):
        if self._lb_open:
            self._var.set(self._lb.get(tk.ACTIVE))
            self._lb.destroy()
            self._lb_open = False
            self.icursor(tk.END)

    def _select_left_click(self, event: tk.Event):
        if self._lb_open:
            selected_index = self._lb.curselection()

            if selected_index:
                index = selected_index[0]
                self._var.set(self._lb.get(index))
                self.icursor(tk.END)
                self._lb.destroy()
                self._lb_open = False
                self.focus_set()  # Set focus back to the entry widget

    def _up_down(self, event: tk.Event):
        if self._lb_open:
            if self._lb.curselection() == ():
                index = -1
            else:
                index = self._lb.curselection()[0]

            lb_size = self._lb.size()

            if index > 0 and event.keysym == "Up":
                self._lb.select_clear(first=index)
                index = str(index - 1)
                self._lb.selection_set(first=index)
                self._lb.activate(index)
            elif index < lb_size - 1 and event.keysym == "Down":
                self._lb.select_clear(first=index)
                index = str(index + 1)
                self._lb.selection_set(first=index)
                self._lb.activate(index)

    def _listbox_select(self, event: tk.Event):
        if self._lb_open:
            selected_index = self._lb.curselection()

            if selected_index:
                index = selected_index[0]
                self._var.set(self._lb.get(index))
                self.icursor(tk.END)
                self._lb.destroy()
                self._lb_open = False
                self.focus_set()  # Set focus back to the entry widget
