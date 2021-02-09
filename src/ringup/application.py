"""Main controller for ringup."""

import tkinter as tk
from tkinter import ttk

from . import views as v
from . import models as m
from . import settings as s

class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title(s.APP_NAME)
        self.resizable(width=False, height=False)
