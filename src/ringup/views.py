"""Views for ringup project."""

import tkinter as tk
from tkinter import ttk
from abc import ABC, abstractmethod

from . import widgets as w

class Form(tk.Frame):

    def __init__(self, parent, model, settings, callbacks, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.settings = settings
        self.callbacks = callbacks
        self.inputs = {}

class ProductForm(Form):
    """The main input form for ringup."""
    def __init__(self, parent, model, settings, callbacks, *args, **kwargs):
        super().__init__(parent, model, settings, callbacks, *args, **kwargs)

        self.current_product = None

        # build the form
        self.product_label = ttk.Label(self, text="PRODUCT")
        self.product_label.grid(row=0, column=0)

        # product specifications section
        specsinfo = tk.LabelFrame(
                self,
                text='Product Specifications',
                bg='khaki',
                padx=10,
                pady=10,
            )

        self.inputs['dummy'] = w.LabelInput(
                specsinfo,
                'Dummy',
                field_spec=None,
                label_args=None,
            )
        self.inputs['dummy'].grid(row=0, column=0)
        specsinfo.grid(row=1, column=0, sticky='we')



