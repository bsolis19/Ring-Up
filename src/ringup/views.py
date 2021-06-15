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

    def _build_layout(self):
        return tk.Frame(
                self,
                padx=10,
                pady=10,
            )

    def _build_control_buttons(self, parent, *cmds):
        for cmd in cmds:
            tk.Button(
                    parent,
                    command=getattr(self, "_{}_cmd".format(cmd)),
                    text=cmd.split('_')[0].title(),
                ).pack(side=tk.LEFT)

    def _build_tabbed_component(self, parent, *tabs):
        component = ttk.Notebook(parent)
        for tab in tabs:
            component.add(
                getattr(
                    self,
                    "_build_{}_frame".format(tab.lower())
                    )(component),
                text=tab.title(),
            )
        return component

    def _build_description_frame(self, parent):
        container = tk.Frame(parent)
        container.pack_propagate(False)
        textbox = tk.Text(container)
        textbox.pack()
        return container

    def _build_details_frame(self, parent):
        container = tk.Frame(parent)
        dict_view = w.DictView(
                container,
                self.model.custom_attributes,
            )
        dict_view.pack()
        # table_component = w.EntryPairTable(
        #         container,
        #         self.model.custom_attributes,
        #         'Detail',
        #         'Value'
        #     )
        # table_component.pack(fill=tk.X)
        return container

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

    def _is_changed(self, field):
        current_value = getattr(self.model, field)
        type_ = type(current_value)
        try:
            new_value = type_(self.inputs[field].get())
            return current_value != new_value
        except ValueError:
            return True

    def _build_modal(self):
        return tk.Toplevel(self.winfo_toplevel())

    def _cancel_cmd(self):
        self._close_window()

    def _close_window(self):
        self.winfo_toplevel().destroy()


class ProductForm(Form):
    """The main input form for ringup."""
    def __init__(self, parent, model, settings, callbacks, *args, **kwargs):
        super().__init__(parent, model, settings, callbacks, *args, **kwargs)

        # Data
        self.header_var = tk.StringVar(value=self.model.name)

        # Containers
        header_container = tk.Frame(self)
        layout = self._build_layout()

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
        tabs = self._build_tabbed_component(
                layout,
                'details',
                'addons',
                'description',
            )
        tabs.grid(columnspan=2, rowspan=3)
        tabs.grid(row=3, column=0)

        # output
        profit_output_component = self._build_profit_output(layout)
        profit_output_component.grid(row=3, column=2)
        price_output_component = self._build_price_output(layout)
        price_output_component.grid(row=4, column=2)

        layout.rowconfigure(5, weight=1)
        layout.pack()

    def _build_addons_frame(self, parent):
        container = tk.Frame(parent)
        group_container = tk.Listbox(container, font=('Calibri', 16))
        self.load_addons(group_container)
        group_container.pack()
        btns_container = tk.Frame(container)
        self._build_control_buttons(
                btns_container,
                'add_addon',
                'edit_addon',
                'delete_addon',
            )
        btns_container.pack(side=tk.BOTTOM)
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

    def _reload_output(self, *args):
        self.profit_output.load()
        self.price_output.load()

    def _add_addon_cmd(self):
        print('addon clicked')
        self._open_add_addon_window()

    def _edit_addon_cmd(self):
        print('edit clicked')

    def _delete_addon_cmd(self):
        print('delete clicked')

    def _open_add_addon_window(self):
        new_window = self._build_modal()
        AddonForm(new_window, self.model, 'new', None, None).pack()


class AddonForm(Form):
    """The addon input form for ringup."""
    def __init__(
            self,
            parent,
            model,
            cmd_type,
            settings,
            callbacks,
            *args,
            **kwargs):
        super().__init__(parent, model, settings, callbacks, *args, **kwargs)
        parent.title(
                '{} Addon for {}'.format(cmd_type.title(), self.model.name)
             )

        # Containers
        header_container = tk.Frame(self)
        btns_container = tk.Frame(self)
        layout = self._build_layout()

        # Header
        header = tk.Label(
                header_container,
                text="New Addon",
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

        self.inputs['waste'] = w.LabelInput(
                layout,
                'Waste:',
                input_args={'width': 3},
            )
        self.inputs['waste'].grid(row=2, column=1)
        self.inputs['waste'].set(self.model.waste)

        # tabbed sections
        tabs = self._build_tabbed_component(layout, 'details', 'description')
        tabs.grid(columnspan=2, rowspan=3)
        tabs.grid(row=3, column=0)

        # control buttons
        self._build_control_buttons(btns_container, 'cancel', 'apply_addon')

        layout.pack()
        btns_container.pack(anchor=tk.E)

    def _apply_addon_cmd(self):
        self._write_changes()
        self._close_window()

    def _write_changes(self):
        try:
            for field, value in self.inputs.items():
                setattr(self.model, field, value)
        except ValueError:
            # TODO Handle invalid data
            pass
