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

invalid_type_product_data_set = (
        {'title': None, 'cost': 3.04, 'description': 'foo'},
        {'title': 'Number', 'cost': None, 'description': 'foo'},
    )

invalid_value_product_data_set = (
        {'title': 'Foo', 'cost': -3.40, 'description': 'bar'},
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
    args = (p.get('title'), p.get('cost'), p.get('description'))
    return 'title: {}, cost: {}, description: {}'.format(*args)


def id_costformula_idata_func(fixture_value):
    """A function for generating ids."""
    cf = fixture_value
    args = (cf.get('formula'), cf.get('variables'))
    return 'formula: {}, variables: {}'.format(*args)


@pytest.fixture()
def a_product():
    """Return something simple."""
    return Product("Glass", 30, "small sheet")


@pytest.fixture()
def an_addon(a_product):
    """Return some simple addon."""
    return Addon(a_product, "Bevel Finish", 3.49, "2-inch")


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
        assert p.title == "Glass"
        assert p.cost == 30
        assert p.description == "small sheet"

        p_with_new_attr = Product(p.title, p.cost, p.description, size="48x96")
        assert p_with_new_attr.size == "48x96"

    def test_member_mutate(self, a_product):
        """Check .field = value functionality of Product."""
        NEW_TITLE = "Foo"
        NEW_COST = 5
        NEW_DESCRIPTION = "foo description"

        p = a_product
        assert (p.title, p.cost, p.description) !=\
            (NEW_TITLE, NEW_COST, NEW_DESCRIPTION)

        p.title = NEW_TITLE
        p.cost = NEW_COST
        p.description = NEW_DESCRIPTION

        assert (p.title, p.cost, p.description) ==\
            (NEW_TITLE, NEW_COST, NEW_DESCRIPTION)

    def test_defaults(self, a_product):
        """Using no optional parameters should invoke defaults."""
        p = a_product
        p1 = Product(p.title, p.cost)
        p2 = Product(p.title, p.cost, "")
        assert p1 == p2

    def test_cost_as_CostFormula(self, a_product, a_costformula):
        """cost attribute should return cost of costfomula."""
        p = a_product
        assert a_costformula.get_cost() == 6
        p.cost = a_costformula

        assert p.cost == 6

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
        assert a.title == a_product.title + " +Bevel Finish"
        assert a.cost == round(a_product.cost + 3.49, 2)
        assert a.description == a_product.description + " " + \
            a_product.title + " " + "2-inch Bevel Finish"

        a_with_new_attr = Addon(
                a_product,
                a.addontitle,
                a.addoncost,
                a.addondescription,
                bevel_size=2,
            )
        assert a_with_new_attr.bevel_size == 2

    def test_defaults(self, an_addon):
        """Using no optional parameters should invoke defaults."""
        a = an_addon
        a1 = Addon(a.product, a.addontitle, a.addoncost)
        a2 = Addon(a.product, a.addontitle, a.addoncost, "")

        assert a1 == a2

    def test_member_mutate(self, an_addon):
        """Check .field = value functionality of Addon."""
        NEW_TITLE = "Foo"
        NEW_COST = 5
        NEW_DESCRIPTION = "foo description"

        a = an_addon
        assert (a.title, a.cost, a.description) != \
            (NEW_TITLE, NEW_COST, NEW_DESCRIPTION)

        a.title = NEW_TITLE
        a.cost = NEW_COST
        a.description = NEW_DESCRIPTION

        assert (a.addontitle, a.addoncost, a.addondescription) == \
            (NEW_TITLE, NEW_COST, NEW_DESCRIPTION)

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
