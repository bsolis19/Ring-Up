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
        self.new_entry = None
        self._build()

    def _build(self):
        self._add_controls(self).pack()
        self._add_data(self, self.data)

    def _add_controls(self, parent):
        container = tk.Frame(parent)
        self.new_entry = EntryPair(container)
        add_btn = tk.Button(
                container,
                text="Add",
                command=self.add_entry_cmd,
            )

        self.new_entry.grid(column=0)
        add_btn.grid(column=1, row=0)

        return container

    def _add_data(self, parent, data):
        for key, value in data.items():
            container = tk.Frame(parent)
            labelInput = LabelInput(
                    container,
                    key,
                )
            self._add_delete_btn(container, key).grid()
            labelInput.grid(row=0, column=1)
            labelInput.set(value)
            container.pack()
            self.entries.append(labelInput)

    def _add_delete_btn(self, parent, key):
        return tk.Button(
                parent,
                text="Delete",
                command=lambda: self.delete_entry_cmd(key),
            )

    def delete_entry_cmd(self, key):
        self._remove_entry(key)

    def _remove_entry(self, key):
        target = None
        for labelInput in self.entries:
            if(labelInput.label.cget('text') == key):
                target = labelInput
                break
        if (target is not None):
            del self.data[key]
            container = target.master
            self.entries.remove(target)
            container.destroy()

    def _clear_new_entry(self):
        for entry in self.new_entry.widgets:
            entry.delete(0, tk.END)

    def add_entry_cmd(self):
        key = self.new_entry.widgets[0].get().strip().lower()
        if len(key) != 0 and key not in self.data:
            value = self.new_entry.widgets[1].get().strip()
            self.data[key] = value

            self._add_data(self, {key: value})

        self._clear_new_entry()


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
