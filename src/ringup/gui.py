"""GUI implementation for ringup."""

from ringup.views import *
from abc import ABC, abstractmethod
from ringup.settings import *


class ViewFactory():

    @staticmethod
    def create(self, view_name, parent):
        # check parent instance
        pass


class GUI():

    def __init__(self, root, title, *args, **kwargs):
        self.root = root
        self.title = APP_NAME
        self._build(*args, **kwargs)

    def _build(self):
        self.createProductForm()
        self.setWindowSize(self.root)

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        try:
            self.root.title(value)
            self._title = value
        except TypeError:
            #TODO Handle Error
            pass

    def setWindowSize(self, window, width=WINDOW_WIDTH, height=WINDOW_HEIGHT):
       window.geometry('%sx%s' % (width, height))

    def activate(self, window=None):
        if window:
            window.mainloop()
        else:
            self.root.mainloop()

    def createProductForm(self):
        main_form = ProductForm(tk.Frame, self.root)
        main_form.grid()


