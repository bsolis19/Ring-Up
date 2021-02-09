"""Views for ringup project."""

import tkinter as tk
from tkinter import ttk

from . import widgets as w

class ProductForm(tk.Frame):
    """The main input form for ringup."""

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.inputs = {}

