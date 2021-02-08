"""Widgets for ringup GUI."""

import tkinter as tk
from tkinter import ttk

class LabelInput(tk.Frame):
    """A widget containing a label and input together."""

    def __init__(
            self,
            parent,
            label='',
            input_class=ttk.Entry,
            input_var=None,
            input_args=None,
            label_args=None,
            **kwargs,
            )
        super().__init__(parent, **kwargs)
        input_args = input_args or {}
        label_args = label_args or {}
        self.variable = input_var

        self.label = ttk.Label(self, text=label, **label_args)
        self.label.grid(row=0, column=0, sticky=(tk.N + tk.S))
        input_args["textvariable"] = input_var
        self.input = input_class(self, **input_args)
        self.input.grid(row=0, column=1, sticky=(tk.N + tk.S))
        #self.rowconfigure(0, weight=1)


    # Create default behavior for grid invocation
    def grid(self, sticky=(tk.N + tk.S), **kwargs):
        super().grid(sticky=sticky, **kwargs)


    # Create wrapper method for the input class' get()
    def get(self):
        try:
            if self.variable:
                return self.variable.get()
            elif type(self.input) == tk.Text:
                return self.input.get('1.0', tk.END)
            else:
                return self.input.get()
        except (TypeError, tk.TclError):
            # happens when numeric fields are empty.
            return ''

    # Create wrapper method for the input class' set()
    def set(self, value, *args, **kwargs):
        if type(self.variable) == tk.BooleanVar:
            self.variable.set(bool(value))
        elif self.variable:
            self.variable.set(value, *args, **kwargs)
        elif type(self.input) in (ttk.Checkbutton, ttk.Radiobutton):
            if value:
                self.input.select()
            else:
                self.input.deselect()
            elif type(self.input) == tk.Text:
                self.input.delete('1.0', tk.END)
                self.input.insert('1.0', value)
            else: # input must be an Entry-type widget with no variable
                self.input.delete(0, tk.END)
                self.input.insert(0, value)

