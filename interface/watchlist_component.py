import tkinter as tk
import typing
from tkinter.font import ITALIC

from models import *

from interface.styling import *
from interface.autocomplete_widget import Autocomplete
from interface.scrollable_frame import ScrollableFrame

from database import WorkspaceData


class Watchlist(tk.Frame):
    def __init__(self, binance_contracts: typing.Dict[str, Contract], bitmex_contracts: typing.Dict[str, Contract],
                 *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.db = WorkspaceData()

        # Set weight for column 0 to make it expand or shrink
        self.columnconfigure(0, weight=1)

        self.binance_symbols = list(binance_contracts.keys())
        self.bitmex_symbols = list(bitmex_contracts.keys())

        # Set border width and relief for the entire Watchlist frame
        self.config(bd=2, relief=tk.GROOVE)

        self._commands_frame = tk.Frame(self, bg="#0B1425")
        self._commands_frame.pack(side=tk.TOP, fill=tk.X, padx=0, pady=0)

        self._table_frame = tk.Frame(self, bg="#091B32")
        self._table_frame.pack(side=tk.TOP, fill=tk.X, padx=0, pady=0)

        self._commands_frame.config(bd=4, relief=tk.GROOVE)

        self._binance_label = tk.Label(self._commands_frame, text="Binance", bg="#191B32", fg=FG_COLOR, font=BOLD_FONT, bd=5, relief=tk.GROOVE)
        self._binance_label.grid(row=0, column=0, sticky="ew")

        self._binance_entry = Autocomplete(self.binance_symbols, self._commands_frame, fg=FG_COLOR, justify=tk.CENTER,
                                                                bg="#291B32", highlightthickness=False, bd=3)

        self._binance_entry.bind("<Return>", self._add_binance_symbol)
        self._binance_entry.grid(row=1, column=0, padx=50, pady=5, sticky="ew")

        self._bitmex_label = tk.Label(self._commands_frame, text="Bitmex", bg="#591B32", fg=FG_COLOR, font=BOLD_FONT, bd=5, relief=tk.GROOVE)
        self._bitmex_label.grid(row=0, column=1, sticky="ew")

        self._bitmex_entry = Autocomplete(self.bitmex_symbols, self._commands_frame, fg=FG_COLOR, justify=tk.CENTER,
                                                                bg="#691B32", highlightthickness=False, bd=3)
        self._bitmex_entry.bind("<Return>", self._add_bitmex_symbol)
        self._bitmex_entry.grid(row=1, column=1, padx=50, pady=5, sticky="ew")

        # Center the _commands_frame columns
        self._commands_frame.columnconfigure(0, weight=1)
        self._commands_frame.columnconfigure(1, weight=1)

        self.body_widgets = dict()

        self._headers = ["symbol", "exchange", "bid", "ask", "remove"]

        self._headers_frame = tk.Frame(self._table_frame)

        self._col_width = 13

        # Creates the headers dynamically

        for idx, h in enumerate(self._headers):
            if h != "remove":
                header = tk.Label(self._headers_frame, text=h.capitalize(), bg="#091B32",
                                  fg=FG_COLOR, font=GLOBAL_FONT2, width=self._col_width, bd=1, relief=tk.GROOVE)
            else:
                header = tk.Label(self._headers_frame, text="", bg="#091B32",
                                  fg=FG_COLOR, font=GLOBAL_FONT2, width=self._col_width)

            header.grid(row=0, column=idx)

        header = tk.Label(self._headers_frame, text="", bg="#091B32",
                          fg=FG_COLOR, font=GLOBAL_FONT2, width=2)
        header.grid(row=0, column=len(self._headers))

        self._headers_frame.pack(side=tk.TOP, anchor="nw", pady=(0, 0), padx=4)  # Adjust the pady value as needed

        # Creates the table body

        self._body_frame = ScrollableFrame(self._table_frame, bg="#0F2E57", height=250, bd=4, relief=tk.SOLID, borderwidth=1)
        self._body_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Add keys to the body_widgets dictionary, the keys represent columns or data related to a column
        # You could also have another logic: instead of body_widgets[column][row] have body_widgets[row][column]
        for h in self._headers:
            self.body_widgets[h] = dict()
            if h in ["bid", "ask"]:
                self.body_widgets[h + "_var"] = dict()

        self._body_index = 0

        # Loads the Watchlist symbols saved to the database during a previous session
        saved_symbols = self.db.get("watchlist")

        for s in saved_symbols:
            self._add_symbol(s['symbol'], s['exchange'])

    def _remove_symbol(self, b_index: int):

        for h in self._headers:
            self.body_widgets[h][b_index].grid_forget()
            del self.body_widgets[h][b_index]

    def _add_binance_symbol(self, event):
        symbol = event.widget.get()

        if symbol in self.binance_symbols:
            self._add_symbol(symbol, "Binance")
            event.widget.delete(0, tk.END)

    def _add_bitmex_symbol(self, event):
        symbol = event.widget.get()

        if symbol in self.bitmex_symbols:
            self._add_symbol(symbol, "Bitmex")
            event.widget.delete(0, tk.END)

    def _add_symbol(self, symbol: str, exchange: str):

        b_index = self._body_index

        self.body_widgets['symbol'][b_index] = tk.Label(self._body_frame.sub_frame, text=symbol, bg="#0E294A",
                                                        fg=FG_COLOR, font=GLOBAL_FONT2, width=12, bd=5, relief=tk.GROOVE, height=2)
        self.body_widgets['symbol'][b_index].grid(row=b_index, column=0)

        self.body_widgets['exchange'][b_index] = tk.Label(self._body_frame.sub_frame, text=exchange, bg="#1D2C53", bd=5, relief=tk.GROOVE,
                                                          fg=FG_COLOR, font=GLOBAL_FONT2, width=12, height=2)
        self.body_widgets['exchange'][b_index].grid(row=b_index, column=1)

        self.body_widgets['bid_var'][b_index] = tk.StringVar()
        self.body_widgets['bid'][b_index] = tk.Label(self._body_frame.sub_frame,
                                                     textvariable=self.body_widgets['bid_var'][b_index],
                                                     bg="#2D2C53", fg=FG_COLOR, font=GLOBAL_FONT2, width=12, bd=5, relief=tk.GROOVE, height=2)
        self.body_widgets['bid'][b_index].grid(row=b_index, column=2)

        self.body_widgets['ask_var'][b_index] = tk.StringVar()
        self.body_widgets['ask'][b_index] = tk.Label(self._body_frame.sub_frame,
                                                     textvariable=self.body_widgets['ask_var'][b_index],
                                                     bg="#3D2C53", fg=FG_COLOR, font=GLOBAL_FONT2, width=12, bd=5, relief=tk.GROOVE, height=2)
        self.body_widgets['ask'][b_index].grid(row=b_index, column=3)

        self.body_widgets['remove'][b_index] = tk.Button(self._body_frame.sub_frame, text="Remove",
                                                         bg="#C20F1C", fg=FG_COLOR, font=GLOBAL_FONT2, bd=3,
                                                         command=lambda: self._remove_symbol(b_index), width=14, height=2)
        self.body_widgets['remove'][b_index].grid(row=b_index, column=4)

        self._body_index += 1

