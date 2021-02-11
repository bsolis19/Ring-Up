"""Views for ringup project."""

import tkinter as tk
from tkinter import ttk
from abc import ABC, abstractmethod

from . import widgets as w

class ProductForm(ABC):
    """The main input form for ringup."""

    def __init__(self, container_class, parent, *args, **kwargs):
        self.container = container_class(parent, *args, **kwargs)

class TKProductForm(ProductForm):

    def grid(self, *args, **kwargs):
        self.container.grid(*args, **kwargs)

    def layout(self):
        pass
