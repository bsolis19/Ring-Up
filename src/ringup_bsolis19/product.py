import uuid

from . import models as m

DEFAULT_MARGIN = .75


class ProductBuilder:
    @staticmethod
    def build_blank_product():
        return m.Product('0', '0', '', 0)

    @staticmethod
    def build_product(*args, **kwargs):
        return m.Product(*args, **kwargs)

    @staticmethod
    def build_addon(*args, **kwargs):
        return m.Addon(*args, **kwargs)


class ProductManager:
    """Manager of product data"""

    product_builder = ProductBuilder

    def __init__(self):
        self.product = ProductManager.product_builder.build_blank_product()
        self.complete_product = self.product

    def create_product(self, sku, name, cost, **extras):
        self.product = ProductManager.product_builder\
                .build_product(
                        self._gen_id(),
                        sku,
                        name,
                        cost,
                        **extras
                        )
        self.complete_product = self.product
        return self

    def create_addon(self, sku, name, cost, **extras):
        self.complete_product = ProductManager.product_builder\
                .build_addon(
                        self.product,
                        self._gen_id(),
                        sku,
                        name,
                        cost,
                        **extras
                        )
        return self

    def get_product(self):
        return self.complete_product

    def calculate_price(self, margin=DEFAULT_MARGIN):
        return self.complete_product.calculate_price(margin)

    def get_addons(self):
        return self.product.addons

    def get_addon(self, id_=''):
        if id_:
            return self.product.get_addon(id_)
        if len(self.complete_product.addons) != 0:
            return self.complete_product


    def remove_addon(self, id_):
        if self.product.addons.get(id_, None) is None:
            return self

        if self.complete_product.id_ is id_:
            self.complete_product = self.complete_product.product

        self.complete_product.remove_addon(id_)
        return self

    def _gen_id(self):
        return str(uuid.uuid4())
