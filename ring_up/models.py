from abc import ABCMeta, abstractmethod
from constants import HomeProductValues as HPConst

class Product(metaclass=ABCMeta):
	
	@property
	@abstractmethod
	def title(self):
		pass

	@title.setter
	def title(self, val):
		self._title_setter(val)
	
	@abstractmethod
	def _title_setter(val):
		pass

	@property
	@abstractmethod
	def price(self):
		pass
	

class HomeProduct(Product):
	
	def __init__(self):
		self.product = product

	@property
	@abstractmethod
	def theme(self):
		pass

	@property
	@abstractmethod
	def size(self):
		pass
	
class WallMirror(HomeProduct):

	def __init__(self,
		     bevel=HPConst.wall_mirror_bevel_default, 
		     thickness=HPConst.wall_mirror_thickness_default,
		     size,
		     theme,
		     title,
		     price,
		    ):
		

	@property
	def bevel(self):
		return self.bevel

	@bevel.setter
	def bevel(self, bevel_length):
		self.bevel = bevel_length

	@property
	def thickness(self):
		return self.thickness

	@thickness.setter
	def thickness(self, thickness):
		self.thickness = thickness
	

if __name__ == "__main__":
	mirr = WallMirror()
	print(mirr.price)
