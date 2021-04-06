"""Widgets for ringup GUI."""

import tkinter as tk

from ringup.lib.observables import ObserverMixin

DEFAULT_FONT = ("Calibri", 18)


class LabelObserverOutput(tk.Label, ObserverMixin):
    def __init__(self, parent, model, output_data, label_args=None):
        super().__init__(parent, **label_args)
        self.model = model
        self.model.registerObserver(self)
        self.get_output_data = output_data

    def load(self):
        # self.config(text=str(self.model.calculate_price(self.margin)))
        self.config(text=str(self.get_output_data(*self.output_args)))

    @property
    def output_args(self):
        return tuple()


class MoneyOutput(LabelObserverOutput):
    def __init__(self, parent, model, amount, margin, label_args=None):
        super().__init__(parent, model, amount, label_args)
        self.margin = margin
        self.load()

    @property
    def output_args(self):
        return tuple([self.margin])

    @property
    def margin(self):
        return float(self._margin.get())

    @margin.setter
    def margin(self, value):
        self._margin = value


class ProfitOutput(MoneyOutput):
    def __init__(self, parent, model, margin, label_args=None):
        super().__init__(
                parent,
                model,
                model.calculate_profit,
                margin,
                label_args
            )


class PriceOutput(MoneyOutput):
    def __init__(self, parent, model, margin, label_args=None):
        super().__init__(
                parent,
                model,
                model.calculate_price,
                margin,
                label_args
             )


class EntryPairTable(tk.Frame):
    MORE = 1
    def __init__(self, parent, data, *headers):
        super().__init__(parent)
        self._in_line_count = 0
        self.data = data

        header_labels = self._build_pair(tk.Label, *headers)
        self._display_headers(*header_labels)

        entry_rows = self._build_rows()
        self._display_body(*entry_rows)

        self.append_empty_entries()
        self.control_btns = self._build_clickable_control_txt('add_more', 'remove_last')

    def _build_pair(self, class_, *txt):
        widget1 = class_(self)
        widget2 = class_(self)
        for i, widget in enumerate((widget1, widget2)):
            if txt and class_ == tk.Label:
                widget.config(text=txt[i])
            elif txt and class_ == tk.Entry:
                widget.insert(0, txt[i])
        return widget1, widget2

    def _display_headers(self, *headers):
        for j, header in enumerate(headers):
            header.grid(row=0, column=j)

    def _build_rows(self):
        rows = list()
        for key, value in self.data.items():
            rows.append(self._build_pair(
                    tk.Entry,
                    key,
                    value,
                )
            )
            self._in_line_count += 1
        return rows

    def _display_body(self, *rows):
        # first row used by headers
        for i, row in enumerate(rows, 1):
            for j, entry in enumerate(row):
                entry.grid(
                    row=i,
                    column=j,
                )

    def append_empty_entries(self):
        row = self._in_line_count + 1
        empty1, empty2 = self._build_pair(class_=tk.Entry)
        empty1.grid(row=row, column=0)
        empty2.grid(row=row, column=1)
        self._in_line_count += 1

    def _add_more_cmd(self):
        self._add_extra_entries()
        self._relocate_control_btns()

    def _add_extra_entries(self):
        for _ in range(self.MORE):
            self.append_empty_entries()

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
