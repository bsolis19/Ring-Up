"""Views for ringup project."""

import tkinter as tk
from tkinter import ttk
from abc import ABC, abstractmethod

from . import widgets as w

class ProductForm(ABC):
    """The main input form for ringup."""

    @abstractmethod
    def __init__(self, container_class, parent, *args, **kwargs):
        self.container = container_class(parent)

class TKProductForm(ProductForm):
