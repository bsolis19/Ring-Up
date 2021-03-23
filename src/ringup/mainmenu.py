import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from functools import partial

class GenericMainMenu(tk.Menu):
    """The application's main menu."""

    def __init__(self, parent, settings, callbacks, **kwargs):
        """Constructor for MainMenu

        arguments:
            parent  -   The parent widget
            settings    -   a dict containing Tkinter variables
            callbacks   -   a dict containing Python callbacks
        """

        super().__init__(parent, **kwargs)
        self.settings = settings
        self.callbacks = callbacks
        self._build_menu()
        self._bind_accelerators()

    def _build_menu(self):
        # the file menu
        file_menu = tk.Menu(self, tearoff=False)
        file_menu.add_command(
                label='Select file...',
                command=self.callbacks['file->select'],
                accelerator='Ctrl+O'
            )
        file_menu.add_separator()
        file_menu.add_command(
                label='Quit',
                command=self.callbacks['file->quit'],
                accelerator='Ctrl+Q'
            )
        self.add_cascade(
                label='File',
                menu=file_menu
            )

        # options menu

        # font size submenu

        # help menu

    def get_keybinds(self):
        return {
                '<Control-o>': self.callbacks['file->select'],
                '<Control-q>': self.callbacks['file->quit'],
                '<Control-n>': self.callbacks['new_product'],
                '<Control-l>': self.callbacks['show_productlist'],
            }

    @staticmethod
    def _argstrip(function, *args):
        return function()

    def _bind_accelerators(self):
        keybinds = self.get_keybinds()
        for key, command in keybinds.items():
            self.bind_all(
                    key,
                    partial(
                        self._argstrip,
                        command,
                    )
                )

    def show_about(self):
        """Show the about dialog."""
        pass


class MacOSMainMenu(GenericMainMenu):
    """
    Differences for MacOS:

        - create app menu
        - move about to app menu, remove 'help'
        - remove redundant quit command
        - change accellerators to Commnand-[]
        - add view menu for font options
        - add window menu for navigation commands
    """

    def _build_menu(self):
        app_menu = tk.Menu(self, tearoff=False, name='apple')
        app_menu.add_command(
                label='About [APP_NAME]',
                command=self.show_about,
            )
        self.add_cascade(
                label='[APP_NAME]',
                menu=app_menu,
            )
        file_menu = tk.Menu(self,tearoff=False)
        file_menu.add_command(
                label="Select file...",
                command=self.callbacks['file->select'],
                accelerator='Cmd-O',
            )
        self.add_cascade(
                label='File',
                menu=file_menu
            )

        # view menu
        view_menu = tk.Menu(self, tearoff=False)
        # font size submenu
        font_size_menu = tk.Menu(view_menu, tearoff=False)
        for size in range(6, 17, 1):
            font_size_menu.add_radiobutton(
                    label = size,
                    value = size,
                    variable=self.settings['font size']
                )
        view_menu.add_cascade(
                label='Font size',
                menu=font_size_menu,
            )

        # window menu
        window_menu = tk.Menu(self, name='window', tearoff=False)
        window_menu.add_command(
                label='Product List',
                command=self.callbacks['show_productlist'],
                accelerator='Cmd-L',
            )
        window_menu.add_command(
                label='New Product',
                command=self.callbacks['new_product'],
                accelerator='Cmd-N',
            )
        self.add_cascade(
                label='Window',
                menu=window_menu,
            )

    def get_keybinds(self):
        return {
                '<Command-o>': self.callbacks['file->select'],
                '<Command-n>': self.callbacks['new_product'],
                '<Command-l>': self.callbacks['show_productlist'],
            }

def get_main_menu_for_os(os_name):
    menus = {
            'Darwin': MacOSMainMenu,
        }

    return menus.get(os_name, GenericMainMenu)
