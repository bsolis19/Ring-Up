import uuid

from .builder import ProductBuilder

class Driver:
    """Core processor of product data"""
    product_builder = ProductBuilder()

    def create_product(self, sku, name, cost, **extras):
        self.product = Driver.product_builder.build_product(self._gen_id(), sku, name, cost, **extras)
        self.complete_product = self.product
        return self

    def create_addon(self, sku, name, cost, **extras):
        self.complete_product = Driver.product_builder.build_addon(self.product, self._gen_id(), sku, name, cost, **extras)
        return self

    def calculate_price(self, margin=DEFAULT_MARGIN):
        return self.complete_product.calculate_price(margin)

    def get_addons(self):
        return self.product.addons

    def get_addon(self, id_):
        return self.product.addons.get(id_, None)

    def remove_addon(self, id_):
        if self.product.addons.get(id_, None) is None:
            return

        if self.complete_product.id_ is id_
            self.complete_product = self.complete_product.product

        self.complete_product.remove_addon(id_)

    def _gen_id(self):
        return str(uuid.uuid4())


