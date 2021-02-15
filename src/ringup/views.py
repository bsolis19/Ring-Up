"""Views for ringup project."""

import tkinter as tk
from tkinter import ttk
from abc import ABC, abstractmethod

from . import widgets as w

class Form():

    def __init__(self, container_class, parent, model, *args, **kwargs):
        self.container = container_class(parent, *args, **kwargs)
        self.model = model
        self.inputs = {}

class ProductForm(Form):
    """The main input form for ringup."""

    def grid(self, *args, **kwargs):
        self.container.grid(*args, **kwargs)

    def layout(self):
        pass

    def buildProperties(self):


    def buildAddonsEntries(self)


