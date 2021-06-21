"""Main controller for ringup."""

import tkinter as tk

from . import views as v
from . import models as m
from . import settings as s
from .mainmenu import get_main_menu_for_os


class Application(tk.Tk):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title(s.APP_NAME)
        self.geometry('%sx%s' % (s.WINDOW_WIDTH, s.WINDOW_HEIGHT))

        # data model
        self.data_model = m.Product(
                '1001',
                '12r',
                'Dozen Roses',
                29.99,
                color='red',
                origin='Mexico'
            )

        # settings model & settings
        config_dir = s.CONFIG_DIR or '~'
        self.settings_model = m.SettingsModel(path=config_dir)
        self.load_settings()

        self.callbacks = {
                'file->select': self.on_file_select,
                'file->quit': self.quit,
                'show_productlist': self.show_productlist,
                'new_product': self.open_product,
                'on_open_product': self.open_product,
                'on_save': self.on_save,
            }

        # menu
        menu_class = get_main_menu_for_os(s.SYSTEM)
        menu = menu_class(self, self.settings, self.callbacks)
        self.config(menu=menu)

        # templates
        _ = tk.Frame(self, width=200, height=400, background='black')
        _.pack(side=tk.LEFT, fill=tk.Y)

        # product data form
        self.productform = v.ProductForm(
                self,
                self.data_model,
                self.settings,
                self.callbacks,
            )
        self.productform.pack(side=tk.TOP, fill=tk.Y)

    def save_settings(self, *args):
        """Save current settings to file."""

        for key, variable in self.settings.items():
            self.settings_model.set(key, variable.get())
        self.settings_model.save()

    def load_settings(self):
        """Load settings into self.settings dict."""
        vartypes = {
                'bool': tk.BooleanVar,
                'str': tk.StringVar,
                'int': tk.IntVar,
                'float': tk.DoubleVar,
            }

        # create dict of settings variables from model's settings
        self.settings = {}
        for key, data in self.settings_model.variables.items():
            vartype = vartypes.get(data['type'], tk.StringVar)
            self.settings[key] = vartype(value=data['value'])

        # put a trace on the variables to save when changed
        for var in self.settings.values():
            var.trace('w', self.save_settings)

    def on_file_select(self):
        """Handle the file->select action from menu."""

        pass

    def show_productlist(self):
        """Show the productform."""

        self.productform.tkraise()

    def open_product(self):
        pass

    def on_save(self):
        pass
