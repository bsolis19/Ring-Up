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


class DictView(tk.Frame):
    def __init__(self, parent, data):
        super().__init__(parent)
        self.data = data
        self.entries = list()
        self._build()

    def _build(self):
        container = tk.Frame(self)
        for key, value in self.data.items():
            self.entries.append(
                    LabelInput(
                        container,
                        key,
                    )
                )
            self.entries[-1].set(value)
            self.entries[-1].pack()
        container.pack()


class EntryPairTable(tk.Frame):
    MORE_ENTRIES = 1
    def __init__(self, parent, data, *headers):
        super().__init__(parent)
        self._in_line_count = 0
        self.data = data
        self.rows = list()

        self.head = self._build_headers(*headers)
        self.body = self._build_body()

        self._display_head()
        self._display_body()

        self.append_empty_entries()
#        self.control_btns = self._build_clickable_control_txt('add_more', 'remove_last')
#
    def _build_headers(self, lead_title, follow_title):
        return LabelPair(self, lead_title, follow_title)

    def _build_body(self):
       return self._build_and_register_rows()

    def _display_head(self):
        self.head.pack()

    def _build_and_register_rows(self):
        container = tk.Frame(self)
        for key, value in self.data.items():
            self.rows.append(EntryPair(
                    container,
                    key,
                    value,
                )
            )
        return container

    def _display_body(self):
        for row in self.rows:
            row.pack()
        self.body.pack()

    def append_empty_entries(self):
        for i in range(EntryPairTable.MORE_ENTRIES):
            self.rows.append(EntryPair(self.body))
            self.rows[-1].pack()

    def _add_more_cmd(self):
        self._add_extra_entries()
        self._relocate_control_btns()

    def _add_extra_entries(self):
        for _ in range(self.MORE):
            self.append_empty_entries()

class WidgetPair(tk.Frame):
    def __init__(self, parent, class_, *values):
        super().__init__(parent)
        self.widgets = self._build_pair(class_, *values)

    def _build_pair(self, class_, lead_txt='', follow_txt=''):
        lead_widget = class_(self)
        follow_widget = class_(self)
        widgets = (lead_widget, follow_widget)
        if lead_txt and follow_txt:
            txts = (lead_txt, follow_txt)
            for i, widget in enumerate(widgets):
                if class_ == tk.Label:
                    widget.config(text=txts[i])
                elif class_ == tk.Entry:
                    widget.insert(0, txts[i])
        return widgets

    def _display_widgets(self, display_cmd='pack', display_args=None):
        for w in self.widgets:
            getattr(w, display_cmd)(**display_args)

class GridBlock:
    def _display_widgets(self):
        for i, w in enumerate(self.widgets):
            w.grid(column=i, row=0)

class EntryPair(GridBlock, WidgetPair):
    def __init__(self, parent, *values):
        super().__init__(parent, tk.Entry, *values)
        self._display_widgets()

class LabelPair(GridBlock, WidgetPair):
    def __init__(self, parent, *values):
        super().__init__(parent, tk.Label, *values)
        self._display_widgets()

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
