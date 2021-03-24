"""Test the data models."""
from ringup.models import Product, Addon, CostFormula
import pytest

# @pytest.fixture()
# def products_just_a_few():
#    """All titles and costs are unique."""
#    return (
#            Product("stamp", .10),
#            Product("baseball", 29.99),
#            Product("shirt", 3.349)
#            )
#
# @pytest.fixture()
# def a_product():
#    """A simple product."""
#    return Product("Glass", 30, "small sheet")

def args_template_gen(arg_names):
    return ', '.join(map(lambda x: x + ' {}', arg_names))

PRODUCT_PROPERTIES = ('sku', 'name', 'cost', 'description', 'fixedcost', 'waste')
ADDON_PROPERTIES = tuple('product') + tuple(PRODUCT_PROPERTIES)
FORMULA_PROPERTIES = ('formula', 'variables')

PRODUCT_ARGS_TEMPLATE = args_template_gen(PRODUCT_PROPERTIES)
ADDON_ARGS_TEMPLATE = args_template_gen(ADDON_PROPERTIES)
FORMULA_ARGS_TEMPLATE = args_template_gen(FORMULA_PROPERTIES)

invalid_type_product_data_set = (
        {'sku': True, 'name': 'Number', 'cost': 3.04, 'description': 'foo'},
        {'sku': '123', 'name': None, 'cost': 3.04, 'description': 'foo'},
        {'sku': '123', 'name': 'Number', 'cost': None, 'description': 'foo'},
    )

invalid_value_product_data_set = (
        {'sku': '123', 'name': 'Foo', 'cost': -3.40, 'description': 'bar'},
    )

invalid_type_costformula_data_set = (
        {'formula': 4, 'variables': {}},
        {'formula': True, 'variables': {}},
        {'formula': 'f', 'variables': 1},
    )

invalid_value_costformula_data_set = (
        {'formula': 'x/y', 'variables': {'x': 1, 'y': 0}},
    )

invalid_syntax_costformula_data_set = (
        {'formula': '%x', 'variables': {'x': 1}},
    )

invalid_key_costformula_data_set = (
        {'formula': 'x+y', 'variables': {'x': 1}},
    )

def id_product_idata_func(fixture_value):
    """A function for generating ids."""
    p = fixture_value
    args = (p.get(member) for member in PRODUCT_PROPERTIES)
    return PRODUCT_ARGS_TEMPLATE.format(*args)


def id_costformula_idata_func(fixture_value):
    """A function for generating ids."""
    cf = fixture_value
    args = (cf.get(member) for member in FORMULA_PROPERTIES)
    return FORMULA_ARGS_TEMPLATE.format(*args)


@pytest.fixture()
def a_product():
    """Return something simple."""
    return Product("3-16G", "Glass", 30, "small sheet", 0.11, 0.02 )


@pytest.fixture()
def an_addon(a_product):
    """Return some simple addon."""
    return Addon(a_product, "BV2", "Bevel Finish", 3.49, "2-inch")


@pytest.fixture()
def a_costformula():
    """Return something simple."""
    return CostFormula("a+b+c", {'a': 1, 'b': 2, 'c': 3})


@pytest.fixture(params=invalid_type_product_data_set,
                ids=id_product_idata_func)
def invalid_type_product_data(request):
    """Return invalid type data fields as dict."""
    return request.param


@pytest.fixture(params=invalid_value_product_data_set,
                ids=id_product_idata_func)
def invalid_value_product_data(request):
    """Return invalid value data fields as dict."""
    return request.param


@pytest.fixture(params=invalid_type_costformula_data_set,
                ids=id_costformula_idata_func)
def invalid_type_costformula_data(request):
    """Return invalid type data fields as dict."""
    return request.param


@pytest.fixture(params=invalid_value_costformula_data_set,
                ids=id_costformula_idata_func)
def invalid_value_costformula_data(request):
    """Return invalid value data fields as dict."""
    return request.param


@pytest.fixture(params=invalid_syntax_costformula_data_set,
                ids=id_costformula_idata_func)
def invalid_syntax_costformula_data(request):
    """Return invalid value data fields as dict."""
    return request.param


@pytest.fixture(params=invalid_key_costformula_data_set,
                ids=id_costformula_idata_func)
def invalid_key_costformula_data(request):
    """Return invalid value data fields as dict."""
    return request.param


class TestProduct:

    def test_member_access(self, a_product):
        """Check .field functionality of Product."""
        p = a_product
        assert p.sku == '3-16G'
        assert p.name == "Glass"
        assert p.cost == 30
        assert p.description == "small sheet"
        assert p.fixedcost == 0.11
        assert p.waste == 0.02

        p_with_new_attr = Product(p.sku, p.name, p.cost, size="48x96")
        assert p_with_new_attr.get_custom_attribute('size') == "48x96"

    def test_member_mutate(self, a_product):
        """Check .field = value functionality of Product."""
        NEW_NAME = "Foo"
        NEW_COST = 5
        NEW_DESCRIPTION = "foo description"
        NEW_FIXEDCOST = 0.33
        NEW_WASTE = 0.07

        p = a_product
        assert (p.name, p.cost, p.description, p.fixedcost, p.waste) !=\
                (NEW_NAME, NEW_COST, NEW_DESCRIPTION, NEW_FIXEDCOST, NEW_WASTE)

        p.name = NEW_NAME
        p.cost = NEW_COST
        p.description = NEW_DESCRIPTION
        p.fixedcost = NEW_FIXEDCOST
        p.waste = NEW_WASTE

        assert (p.name, p.cost, p.description, p.fixedcost, p.waste) ==\
            (NEW_NAME, NEW_COST, NEW_DESCRIPTION, NEW_FIXEDCOST, NEW_WASTE)

    def test_defaults(self, a_product):
        """Using no optional parameters should invoke defaults."""
        p = a_product
        p1 = Product(p.sku, p.name, p.cost)
        p2 = Product(p.sku, p.name, p.cost, "", 0, 0.0)
        assert p1 == p2

    def test_cost_as_CostFormula(self, a_product, a_costformula):
        """cost attribute should return cost of costfomula."""
        p = a_product
        assert a_costformula.get_cost() == 6
        p.cost = a_costformula

        assert p.cost == 6

    def test_price_property(self, a_product):
        """price should return calculated sell price with default margin of 75%"""
        p = a_product
        assert p.cost == 30
        assert p.fixedcost == 0.11
        assert p.waste == 0.02

        expected = (30 * (1 + 0.02) + 0.11) / (1 - 0.75)
        assert p.price == expected

    def test_new_product_raises_TypeError(self, invalid_type_product_data):
        """Product() should raise an exception with invalid param."""
        with pytest.raises(TypeError):
            Product(**invalid_type_product_data)

    def test_new_product_raises_ValueError(self, invalid_value_product_data):
        """Product() should raise an exception with invalid param."""
        with pytest.raises(ValueError):
            Product(**invalid_value_product_data)


class TestAddon:
    def test_member_access(self, a_product, an_addon):
        """Check .field functionality of Addon."""
        a = an_addon
        assert a.product == a_product
        assert a.name == a_product.name + " +Bevel Finish"
        assert a.cost == round(a_product.cost + 3.49, 2)
        assert a.description == a_product.description + " " + \
            a_product.name + " " + "2-inch Bevel Finish"
        assert a.fixedcost == a_product.fixedcost
        assert a.waste == a_product.waste

        a_with_new_attr = Addon(
                a_product,
                a.addonname,
                a.addoncost,
                a.addondescription,
                bevel_size=2,
            )
        assert a_with_new_attr.get_custom_attribute('bevel_size') == 2

    def test_defaults(self, an_addon):
        """Using no optional parameters should invoke defaults."""
        a = an_addon
        a1 = Addon(a.product, a.addonname, a.addoncost)
        a2 = Addon(a.product, a.addonname, a.addoncost, "")

        assert a1 == a2

    def test_member_mutate(self, an_addon):
        """Check .field = value functionality of Addon."""
        NEW_NAME = "Foo"
        NEW_COST = 5
        NEW_DESCRIPTION = "foo description"

        a = an_addon
        assert (a.name, a.cost, a.description) != \
            (NEW_NAME, NEW_COST, NEW_DESCRIPTION)

        a.name = NEW_NAME
        a.cost = NEW_COST
        a.description = NEW_DESCRIPTION

        assert (a.addonname, a.addoncost, a.addondescription) == \
            (NEW_NAME, NEW_COST, NEW_DESCRIPTION)


    def test_price_property_default_margin(self, an_addon):
        """price should return calculated sell price with default margin of 75%"""
        a = an_addon
        p_cost = a.product.cost
        p_waste = a.product.waste
        p_fixedcost = a.product.fixedcost
        assert a.price == ((p_cost + 3.49) * (1 + p_waste) + p_fixedcost) / (1 - 0.75)

    def test_calculate_price(self, an_addon):
        """calculate_price() should return calculated sell price using margin arg"""
        a = an_addon
        p_cost = a.product.cost
        p_waste = a.product.waste
        p_fixedcost = a.product.fixedcost
        assert a.calculate_price(.60) == ((p_cost + 3.49) * (1 + p_waste) + p_fixedcost) / (1 - 0.60)

    def test_new_addon_raises_TypeError(self, a_product,
                                        invalid_type_product_data):
        """Addon() should raise an exception with invalid param."""
        with pytest.raises(TypeError):
            Addon(a_product, **invalid_type_product_data)

    def test_new_addon_raises_ValueError(self, a_product,
                                         invalid_value_product_data):
        """Addon() should raise an exception with invalid param."""
        with pytest.raises(ValueError):
            Addon(a_product, **invalid_value_product_data)


class TestCostFormula:

    def test_member_access(self, a_costformula):
        """Check .field functionality of CostFormula."""
        cf = a_costformula
        assert cf.variables == {'a': 1, 'b': 2, 'c': 3}
        assert cf.formula == 'a+b+c'

    def test_memeber_mutate(self, a_costformula):
        """Check .field = value functionality of CostFormula."""
        NEW_FORMULA = 'x+y+z'
        NEW_VARIABLES = {'x': 10, 'y': 20, 'z': 30}

        cf = a_costformula
        assert (cf.formula, cf.variables) != (NEW_FORMULA, NEW_VARIABLES)

        cf.variables = NEW_VARIABLES
        cf.formula = NEW_FORMULA

        assert (cf.formula, cf.variables) == (NEW_FORMULA, NEW_VARIABLES)

    def test_lt_comparison(self, a_costformula):
        assert int(a_costformula.get_cost()) > 0
        assert a_costformula > 0

    def test_get_cost(self, a_costformula):
        assert a_costformula.get_cost() == 6

    def test_new_costformula_raises_TypeError(self,
                                              invalid_type_costformula_data):
        """CostFormula() should raise an exceptionwith invalid param."""
        with pytest.raises(TypeError):
            CostFormula(**invalid_type_costformula_data)

    def test_new_costformula_raises_ValueError(self,
                                               invalid_value_costformula_data):
        """CostFormula() should raise an exception with invalid param."""
        with pytest.raises(ValueError):
            CostFormula(**invalid_value_costformula_data)

    def test_new_costformula_raises_SyntaxError(self,
                                                invalid_syntax_costformula_data
                                                ):
        """CostFormula() should raise an exception with invalid param."""
        with pytest.raises(SyntaxError):
            CostFormula(**invalid_syntax_costformula_data)


    def test_new_costformula_raises_KeyError(self,
                                                invalid_key_costformula_data
                                                ):
        """CostFormula() should raise an exception with invalid param."""
        with pytest.raises(KeyError):
            CostFormula(**invalid_key_costformula_data)
