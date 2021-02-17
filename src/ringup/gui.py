"""GUI implementation for ringup."""

from ringup.views import *
from ringup.settings import *


class GUI(tk.Tk):

    def __init__(self, title, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title(title)
        self._build()

    def _build(self):
        self.createProductForm()
        self.setWindowSize(self.root)

    def createProductForm(self):
        main_form = ProductForm(self)
        main_form.grid()


