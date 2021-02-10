"""Main controller for ringup."""

import tkinter as tk
from tkinter import ttk

from . import views as v
from . import models as m
from . import settings as s

class Application():

    def __init__(self, gui, *args, **kwargs):
        self.gui = gui
        self.config(*args, **kwargs)

    #Currently not implemented
    def config(self):
        pass

    def start(self):
        self.gui.activate()


