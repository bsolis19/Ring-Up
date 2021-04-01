"""Views for ringup project."""

import tkinter as tk

from tkinter import ttk

from . import widgets as w


class Form(tk.Frame):

    PROFIT_COLOR = "#118C4F"
    FOCUS_COLOR = "#1D3F6E"

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
        self.header_var = tk.StringVar(value=self.model.name)

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
        self.inputs['sku'] = w.LabelInput(
                layout,
                'SKU:',
                input_args={'width': 12},
            )
        self.inputs['sku'].grid()
        # self.inputs['sku'].columnconfigure(1, weight=1)
        self.inputs['sku'].set(self.model.sku)

        self.inputs['name'] = w.LabelInput(
                layout,
                'Name:',
            )
        self.inputs['name'].grid(row=1, column=0, columnspan=3)
        self.inputs['name'].columnconfigure(1, weight=1)
        self.inputs['name'].set(self.model.name)

        self.inputs['cost'] = w.LabelInput(
                layout,
                'Cost:',
                input_args={'width': 6},
            )
        self.inputs['cost'].grid(row=2, column=0)
        self.inputs['cost'].set(self.model.cost)
        self.inputs['cost'].input_.bind('<FocusOut>', self._set_model_cost)

        self.inputs['fixed_cost'] = w.LabelInput(
                layout,
                'Fixed Cost:',
                input_args={'width': 5},
            )
        self.inputs['fixed_cost'].grid(row=2, column=1)
        self.inputs['fixed_cost'].set(self.model.fixed_cost)
        self.inputs['fixed_cost'].input_\
            .bind('<FocusOut>', self._set_model_fixed_cost)

        self.inputs['waste'] = w.LabelInput(
                layout,
                'Waste :',
                input_args={'width': 3},
            )
        self.inputs['waste'].grid(row=2, column=2)
        self.inputs['waste'].set(self.model.waste)
        self.inputs['waste'].input_.bind('<FocusOut>', self._set_model_waste)

        self.inputs['margin'] = w.LabelInput(
                layout,
                'Margin :',
                input_var=tk.DoubleVar(),
                input_args={'width': 3},
            )
        self.inputs['margin'].grid(row=2, column=2)
        self.inputs['margin'].input_.bind('<FocusOut>', self._reload_output)

        # tabbed sections
        tabs = self._build_tabbed_component(layout)
        tabs.grid(columnspan=2, rowspan=3)
        tabs.grid(row=3, column=0)

        # output
        profit_output_component = self._build_profit_output(layout)
        profit_output_component.grid(row=3, column=2)
        price_output_component = self._build_price_output(layout)
        price_output_component.grid(row=4, column=2)

        layout.rowconfigure(5, weight=1)
        layout.pack()

    def _build_tabbed_component(self, parent):
        component = ttk.Notebook(parent)
        component.add(
                self._build_details_frame(component),
                text='Details',
            )
        component.add(
                self._build_addons_frame(component),
                text='Addons',
            )
        component.add(
                self._build_description_frame(component),
                text='Description',
            )
        return component

    def _build_details_frame(self, parent):
        container = tk.Frame(parent)
        table_component = self._build_details_table(container)
        table_component.pack(fill=tk.X)
        return container

    def _build_addons_frame(self, parent):
        container = tk.Frame(parent)
        group_container = tk.Listbox(container, font=('Calibri', 16))
        self.load_addons(group_container)
        group_container.pack()
        btns_container = tk.Frame(container)
        self._build_control_buttons(btns_container)
        btns_container.pack(side=tk.BOTTOM)
        return container

    def _build_description_frame(self, parent):
        container = tk.Frame(parent)
        container.pack_propagate(False)
        textbox = tk.Text(container)
        textbox.pack()
        return container

    def _build_details_table(self, parent):
        container = tk.Frame(parent)
        header1, header2 = self._build_pair(container, 'Detail', 'Value')
        header1.grid()
        header2.grid(row=0, column=1)
        container.columnconfigure(0, weight=1)
        container.columnconfigure(1, weight=1)
        self.load_details(container)
        self.append_empty_detail_entry(container)
        return container

    def _build_price_output(self, parent):
        container = tk.Frame(parent)
        label = tk.Label(
                container,
                text='Sell Price',
                fg=self.FOCUS_COLOR,
                font=('Calibri', 20),
                )
        label.grid(row=0, column=0)
        self.price_output = w.PriceOutput(
                container,
                self.model,
                self.inputs['margin'].variable,
                label_args={
                    'font': ('Calibri', 24),
                    'fg': self.FOCUS_COLOR,
                    },
                )
        self.price_output.grid(row=1, column=0)
        return container

    def _build_profit_output(self, parent):
        container = tk.Frame(parent)
        label = tk.Label(
                container,
                text='Profit',
                fg=self.PROFIT_COLOR,
                font=('Calibri', 20),
                )
        label.grid(row=0, column=0)
        self.profit_output = w.ProfitOutput(
                container,
                self.model,
                self.inputs['margin'].variable,
                label_args={
                    'font': ('Calibri', 24),
                    'fg': self.PROFIT_COLOR,
                    },
                )
        self.profit_output.grid(row=1, column=0)
        return container

    def _build_pair(self, parent, txt1='', txt2='', class_=tk.Label):
        if class_ == tk.Label:
            w1 = class_(parent, text=txt1)
            w2 = class_(parent, text=txt2)
        elif class_ == tk.Entry:
            w1 = class_(parent)
            w1.insert(0, txt1)
            w2 = class_(parent)
            w2.insert(0, txt2)
        else:
            raise ValueError('Widget pair could not be created')
        return w1, w2

    def load_details(self, container):
        details = self._get_details()
        self._display_details(container, details)

    def _get_details(self):
        return self.model.custom_attributes

    def _display_details(self, parent, details):
        # row 0 used by header text
        current_row = 1
        current_col = 0
        for detail in details:
            detail_entry = tk.Entry(parent)
            value_entry = tk.Entry(parent)
            detail_entry.insert(0, str(detail))
            value_entry.insert(0, str(details[detail]))

            detail_entry.grid(
                    row=current_row,
                    column=current_col,
                )
            current_col += 1
            value_entry.grid(
                    row=current_row,
                    column=current_col,
                )
            current_row += 1
            current_col -= 1

    def append_empty_detail_entry(self, parent):
        # +1 due to header text occupying first row
        row = len(self._get_details()) + 1
        empty1, empty2 = self._build_pair(parent=parent, class_=tk.Entry)
        empty1.grid(row=row, column=0)
        empty2.grid(row=row, column=1)

    def load_addons(self, parent):
        addons = self._get_addons()
        self._display_addons(parent, addons)

    def _get_addons(self):
        return self.model.addons

    def _display_addons(self, parent, addons):
        i = 0
        for addon in addons:
            parent.insert(i, str(addon))
            i += 1

    def _build_control_buttons(self, parent):
        edit_btn = tk.Button(parent, text='Edit')
        add_btn = tk.Button(parent, text='Add')
        delete_btn = tk.Button(parent, text='Delete')

        edit_btn.pack(side=tk.LEFT)
        add_btn.pack(side=tk.LEFT)
        delete_btn.pack(side=tk.LEFT)

    def _set_model_cost(self, *args):
        if self._is_changed('cost'):
            try:
                self.model.cost = float(self.inputs['cost'].get())
            except ValueError:
                # TODO set error message
                pass

    def _set_model_fixed_cost(self, *args):
        if self._is_changed('fixed_cost'):
            try:
                self.model.fixed_cost = float(self.inputs['fixed_cost'].get())
            except ValueError:
                # TODO set error message
                pass

    def _set_model_waste(self, *args):
        if self._is_changed('waste'):
            try:
                self.model.waste = float(self.inputs['waste'].get())
            except ValueError:
                # TODO set error message
                pass

    def _reload_output(self, *args):
        self.profit_output.load()
        self.price_output.load()

    def _is_changed(self, field):
        current_value = getattr(self.model, field)
        type_ = type(current_value)
        try:
            new_value = type_(self.inputs[field].get())
            return current_value != new_value
        except ValueError:
            return True
