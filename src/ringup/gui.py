"""GUI implementation for ringup."""

from ringup.views import *
from abc import ABC, abstractmethod
from ringup.settings import *

class GUI(ABC):

    def __init__(self, root, *args, **kwargs):
        self.root = root
        self.title = APP_NAME
        self._build(*args, **kwargs)

    @abstractmethod
    def activate(self):
        pass
    @abstractmethod
    def createProductForm(self):
        pass

    @property
    def title(self):
        return self._title

    @title.setter
    @abstractmethod
    def title(self, value):
        pass

    @abstractmethod
    def setWindowSize(self, window, width, height):
        pass

    def _build(self):
        self.createProductForm()
        self.setWindowSize(self.root)

class ViewFactory():

    @staticmethod
    def create(self, view_name, parent):
        # check parent instance
        pass


class TKGUI(GUI):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def title(self):
        super().title()

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

    def activate(self):
        self.root.mainloop()

    def createProductForm(self):
        main_form = TKProductForm(tk.Frame, self.root)
        main_form.grid()


