"""Views for ringup project."""

import tkinter as tk
from tkinter import ttk

from . import widgets as w

class Form(tk.Frame):

    def __init__(self, parent, model, settings, callbacks, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.model = model
        self.settings = settings
        self.callbacks = callbacks
        self.inputs = {}


class ProductForm(Form):
    """The main input form for ringup."""
    def __init__(self, parent, model, settings, callbacks, *args, **kwargs):
        super().__init__(parent, model, settings, callbacks, *args, **kwargs)

        self.model = model
        self.header_var = tk.StringVar(value=self.model.title)

        # build the form
        self.header = ttk.Label(self, textvariable=self.header_var)
        self.header.pack()

        # product specifications section
        specsinfo = tk.LabelFrame(
                self,
                text='Product Details',
                padx=10,
                pady=10,
            )

        self.inputs['title'] = w.LabelInput(
                specsinfo,
                'Title:',
                field_spec=None,
                label_args=None,
            )
        # self.inputs['dummy'].grid(row=0, column=0)
        self.inputs['title'].pack()
        # specsinfo.grid(row=1, column=0, sticky='we')
        specsinfo.pack()

        costinfo = tk.LabelFrame(
                self,
                text="Cost",
                bg='red',
                padx=10,
                pady=10,
            )
        self.inputs['margin'] = w.LabelInput(
                costinfo,
                'Margin',
                field_spec=None,
                label_args=None,
            )

        # price output
        self._build_price_output()

    def _build_price_output(self):
        container = tk.Frame(self)
        self.price_label = ttk.Label(container, text='Sell Price:')
        self.price_label.grid(row=0, column=0)
        self.output = w.PriceOutput(container, self.model, self.inputs['margin'].variable)
        self.output.grid(row=0, column=1)
        container.pack(side=tk.BOTTOM, fill=tk.X)
