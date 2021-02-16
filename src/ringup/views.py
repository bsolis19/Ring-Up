"""Views for ringup project."""

import tkinter as tk
from tkinter import ttk
from abc import ABC, abstractmethod

from . import widgets as w

class Form(Tk.Frame):

    def __init__(self, parent, model, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.model = model
        self.inputs = {}

class ProductForm(Form):
    """The main input form for ringup."""

    def layout(self):
        pass

    def buildProperties(self):
        pass

    def buildAddonsEntries(self):
        pass


