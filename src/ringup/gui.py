"""GUI implementation for ringup."""

from abc import ABC, abstractmethod

class GUI(ABC):
    @abstractmethod
    def activate(self):
        pass

    @abstractmethod
    def _build(self):
        self._view_factory.create('ProductForm', self._root)

class ViewFactory():

    @staticmethod
    def create(self, view_name, parent):
        # check parent instance


class TKGUI(GUI):
    def __init__(self, tk_instance, *args, **kwargs):
        self._root = tk_instance
        self._build(*args, **kwargs)

    def activate(self):
        self._root.mainloop()

    def _build(self):

