"""Widgets for ringup GUI."""

import tkinter as tk

from ringup.lib.observables import ObserverMixin

DEFAULT_FONT = ("Calibri", 18)

class PriceOutput(tk.Label, ObserverMixin):
    def __init__(self, parent, model, margin, *args, **kwargs):
        super().__init__(parent, text='label', *args, **kwargs)
        self.model = model
        self.margin = margin

    @property
    def margin(self):
        return float(self._margin.get())

    @margin.setter
    def margin(self, value):
        self._margin = value

    def update(self):
        self.text = str(self.model.price(self.margin))


class LabelInput(tk.Frame):
    """A widget containing a label and input together."""

    def __init__(
            self,
            parent,
            label='',
            input_class=tk.Entry,
            input_var=None,
            input_args=None,
            label_args=None,
            **kwargs
            ):
        super().__init__(parent, **kwargs)
        input_args = input_args or {}
        input_args["textvariable"] = input_var
        label_args = label_args or {'font': DEFAULT_FONT}

        self.variable = input_var
        self.label = tk.Label(self, text=label, **label_args)
        self.input_ = input_class(self, **input_args)

        self.label.grid(row=0, column=0)
        self.input_.grid(row=0, column=1, sticky=tk.W+tk.E)

    # Create default behavior for grid invocation
    def grid(self, sticky=(tk.W + tk.E), **kwargs):
        super().grid(sticky=sticky, **kwargs)

    # Create wrapper method for the input class' get()
    def get(self):
        try:
            if self.variable:
                return self.variable.get()
            elif type(self.input_) == tk.Text:
                return self.input_.get('1.0', tk.END)
            else:
                return self.input_.get()
        except (TypeError, tk.TclError):
            # happens when numeric fields are empty.
            return ''

    # Create wrapper method for the input class' set()
    def set(self, value, *args, **kwargs):
        if type(self.variable) == tk.BooleanVar:
            self.variable.set(bool(value))
        elif self.variable:
            self.variable.set(value, *args, **kwargs)
        elif type(self.input_) in (tk.Checkbutton, tk.Radiobutton):
            if value:
                self.input_.select()
            else:
                self.input_.deselect()
        elif type(self.input_) == tk.Text:
            self.input_.delete('1.0', tk.END)
            self.input_.insert('1.0', value)
        else:  # input must be an Entry-type widget with no variable
            self.input_.delete(0, tk.END)
            self.input_.insert(0, value)
