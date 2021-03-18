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

        # Data
        self.model = model
        self.header_var = tk.StringVar(value=self.model.title)

        # Containers
        header_container = tk.Frame(self)
        layout = tk.Frame(
                self,
                padx=10,
                pady=10,
            )

        # Header
        header = tk.Label(
                header_container,
                textvariable=self.header_var,
                font=("Calibri", 24),
            )
        header.pack()
        header_container.pack()

        # Entries
        self.inputs['title'] = w.LabelInput(
                layout,
                'Title:',
            )
        self.inputs['title'].grid(columnspan=3)
        self.inputs['title'].columnconfigure(1, weight=1)
        self.inputs['cost'] = w.LabelInput(
                layout,
                'Cost:',
                input_args={'width': 6},
            )
        self.inputs['cost'].grid(row=1, column=0)
        self.inputs['fixedcost'] = w.LabelInput(
                layout,
                'Fixed Cost:',
                input_args={'width': 5},
            )
        self.inputs['fixedcost'].grid(row=1, column=1)
        self.inputs['waste'] = w.LabelInput(
                layout,
                'Waste :',
                input_args={'width': 3},
            )
        self.inputs['waste'].grid(row=1, column=2)
        self.inputs['margin'] = w.LabelInput(
                layout,
                'Margin :',
                input_args={'width': 3},
            )
        self.inputs['margin'].grid(row=2, column=2)

        # tabbed sections
        tabs = self._build_tabbed_component(layout)
        tabs.grid(columnspan=2, rowspan=3)
        tabs.grid(row=2, column=0)

        # price output
        output_component = self._build_price_output(layout)
        output_component.grid(row=3, column=2)

        layout.rowconfigure(3, weight=1)
        layout.pack()

    def _build_tabbed_component(self, parent):
        component = ttk.Notebook(parent)
        component.add(
                self._build_details_frame(component),
                text='Details',
            )
        component.add(
                self._build_details_frame(component),
                text='Addons',
            )
        component.add(
                self._build_description_frame(component),
                text='Description',
            )
        return component

    def _build_details_frame(self, parent):
        container = tk.Frame(parent, background='red')
        lb = tk.Listbox(container, background='blue')
        lb.pack()
        return container

    def _build_description_frame(self, parent):
        container = tk.Frame(parent, background='red')
        textbox = tk.Text(container, background='blue', height=30, width=30)
        textbox.pack()
        return container

    def _build_price_output(self, parent):
        container = tk.Frame(parent)
        label = tk.Label(
                container,
                text='Sell Price',
                font=('Calibri', 20),
                )
        label.grid(row=0, column=0)
        self.output = w.PriceOutput(
                container,
                self.model,
                self.inputs['margin'].variable,
                label_args={'font': ('Calibri', 24)},
                )
        self.output.grid(row=1, column=0)
        return container
