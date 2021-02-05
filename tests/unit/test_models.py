"""Test the data models."""
from ringup.models import *
import pytest

#@pytest.fixture()
#def products_just_a_few():
#    """All titles and costs are unique."""
#    return (
#            Product("stamp", .10),
#            Product("baseball", 29.99),
#            Product("shirt", 3.349)
#            )
#
#@pytest.fixture()
#def a_product():
#    """A simple product."""
#    return Product("Glass", 30, "small sheet")

invalid_type_data_set = (
        {'title': None, 'cost': 3.04, 'description': 'foo'},
        {'title': 'Number', 'cost': None, 'description': 'foo'},
    )

invalid_value_data_set = (
        {'title': 'Foo', 'cost': -3.40, 'description': 'bar'},
    )

def id_idata_func(fixture_value):
    """A function for generating ids."""
    p = fixture_value
    args = (p.get('title'), p.get('cost'), p.get('description'))
    return 'title: {}, cost: {}, description: {}'.format(*args)

@pytest.fixture()
def a_product():
    """Return something simple."""
    return Product("Glass", 30, "small sheet")

@pytest.fixture(params=invalid_type_data_set, ids=id_idata_func)
def invalid_type_data(request):
    """Return invalid type data fields as dict."""
    return request.param

@pytest.fixture(params=invalid_value_data_set, ids=id_idata_func)
def invalid_value_data(request):
    """Return invalid value data fields as dict."""
    return request.param

class TestProduct:

    def test_member_access(self, a_product):
        """Check .field functionality of Product."""
        p = a_product
        assert p.title == "Glass"
        assert p.cost == 30
        assert p.description == "small sheet"

        p_with_new_attr = Product(p.title, p.cost, p.description, size="48x96")
        assert p_with_new_attr.size == "48x96"

    def test_defaults(self, a_product):
        """Using no optional parameters should invoke defaults."""
        p = a_product
        p1 = Product(p.title, p.cost)
        p2 = Product(p.title, p.cost, "")
        assert p1 == p2

    def test_member_mutate(self, a_product):
        """Check .field = value functionality of Product."""
        NEW_TITLE = "Foo"
        NEW_COST = 5
        NEW_DESCRIPTION = "foo description"

        p = a_product
        assert (p.title, p.cost, p.description) != (NEW_TITLE, NEW_COST, NEW_DESCRIPTION)

        p.title = NEW_TITLE
        p.cost = NEW_COST
        p.description = NEW_DESCRIPTION

        assert (p.title, p.cost, p.description) == (NEW_TITLE, NEW_COST, NEW_DESCRIPTION)

    def test_new_product_raises_TypeError(self, invalid_type_data):
        """Product() should raise an exception with invalid param."""
        with pytest.raises(TypeError):
            Product(**invalid_type_data)

    def test_new_product_raises_ValueError(self, invalid_value_data):
        """Product() should raise an exception with invalid param."""
        with pytest.raises(ValueError):
            Product(**invalid_value_data)

@pytest.fixture()
def an_addon(a_product):
    """Return some simple addon."""
    return Addon(a_product, "Bevel Finish", 3.49, "2-inch bevel")

class TestAddon:
    def test_member_access(self, a_product, an_addon):
        """Check .field functionality of Addon."""
        a = an_addon
        assert a.product == a_product
        assert a.title == a_product.title + " +Bevel Finish"
        assert a.cost == round(a_product.cost + 3.49, 2)
        # TODO assert a.description = "TODO"

        a_with_new_attr = Addon(a_product, a.addontitle, a.addoncost, a.addondescription, bevel_size=2)
        assert a_with_new_attr.bevel_size == 2




