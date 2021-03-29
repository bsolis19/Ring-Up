"""Test the product product_manager."""
from ringup.product import ProductManager
from ringup.models import Product, Addon

import pytest

#def load_tests(name):
#    tests_file = open(name)
#
#def pytest_generate_tests(metafunc):
#    for fixture in metafunc.fixturenames:
#        if fixture.startswith('data_'):
#            tests = load_tests(fixture)
#            metafunc.parametrize(fixture, tests)

product_data_set = {
        'sku': '123Product',
        'name': 'Foo',
        'cost': 123.00,
    }
addon_data_set = {
        'sku': 'AO1',
        'name': 'Bar',
        'cost': 3.00,
    }

BLANK_PRODUCT = Product(0, '0', '', 0.00)
DEFAULT_MARGIN = .75


@pytest.fixture()
def a_blank_product():
    return Product(0, '0', '', 0.00)


@pytest.fixture()
def product_data():
    return product_data_set


@pytest.fixture()
def addon_data():
    return addon_data_set

@pytest.fixture()
def product_manager():
    return ProductManager()

def test_create_product(product_manager, product_data):
    product = product_manager.create_product(**product_data).get_product()
    for key, val in product_data.items():
        assert getattr(product, key) == val

def test_create_addon(product_manager, addon_data):
    addon = product_manager.create_addon(**addon_data).get_addon()
    for key, val in addon_data.items():
        assert getattr(addon, key) == val

def test_get_product_when_nothing_created(product_manager):
    product = product_manager.get_product()
    assert product == BLANK_PRODUCT

def test_get_product_when_product_not_created_and_addon_created(product_manager, addon_data):
    product = product_manager.create_addon(**addon_data).get_product()
    for key, val in addon_data.items():
        assert getattr(product, key) == val

def test_get_product_when_product_and_addon_created(product_manager, product_data, addon_data):
    product = product_manager\
            .create_product(**product_data)\
            .create_addon(**addon_data)\
            .get_product()

    p_id = product.product.id_
    a_id = product.id_

    expected = Addon(
            Product(id_=p_id, **product_data),
            id_=a_id,
            **addon_data)

    assert product == expected

def test_calculate_price_when_nothing_created(product_manager):
    assert product_manager.calculate_price() == 0

def test_calculate_price_when_product_created_and_addon_not_created(product_manager, product_data):
    price = product_manager.create_product(**product_data).calculate_price()

    WASTE = product_data.get('waste', 0)
    FIXED_COST = product_data.get('fixed_cost', 0)
    CALCULATED_COST = product_data.get('cost', 0) * (1 + WASTE)
    TOTAL_COST = CALCULATED_COST + FIXED_COST

    expected = TOTAL_COST / (1 - DEFAULT_MARGIN)

    assert expected == price

def test_calculate_price_when_product_not_created_and_addon_created(product_manager, addon_data):
    price = product_manager.create_addon(**addon_data).calculate_price()

    WASTE = addon_data.get('waste', 0)
    FIXED_COST = addon_data.get('fixed_cost', 0)
    CALCULATED_COST = addon_data.get('cost', 0) * (1 + WASTE)
    TOTAL_COST = CALCULATED_COST + FIXED_COST

    expected = TOTAL_COST / (1 - DEFAULT_MARGIN)

    assert expected == price

def test_calculate_price_when_product_created_and_addon_created(product_manager, product_data, addon_data):
    price = product_manager\
            .create_product(**product_data)\
            .create_addon(**addon_data)\
            .calculate_price()

    A_WASTE = addon_data.get('waste', 0)
    A_FIXED_COST = addon_data.get('fixed_cost', 0)
    A_CALCULATED_COST = addon_data.get('cost', 0) * (1 + A_WASTE)
    A_TOTAL_COST = A_CALCULATED_COST + A_FIXED_COST

    P_WASTE = product_data.get('waste', 0)
    P_FIXED_COST = product_data.get('fixed_cost', 0)
    P_CALCULATED_COST = product_data.get('cost', 0) * (1 + P_WASTE)
    P_TOTAL_COST = P_CALCULATED_COST + P_FIXED_COST

    TOTAL_COST = A_TOTAL_COST + P_TOTAL_COST

    expected = TOTAL_COST / (1 - DEFAULT_MARGIN)

    assert expected == price

def test_get_addons_when_nothing_created(product_manager):
    addons = product_manager.get_addons()

    expected = BLANK_PRODUCT.addons
    assert addons == expected

def test_get_addons_when_product_not_created_and_addon_created(product_manager, addon_data, a_blank_product):
    addons = product_manager.create_addon(**addon_data).get_addons()

    id_ = product_manager.get_product().id_
    expected = Addon(a_blank_product, id_, **addon_data).addons

    assert addons == expected

def test_get_addons_when_product_created_and_addon_created(product_manager, product_data, addon_data, a_blank_product):
    addons = product_manager\
            .create_product(**product_data)\
            .create_addon(**addon_data)\
            .get_addons()

    id_ = product_manager.get_product().id_
    expected = Addon(a_blank_product, id_, **addon_data).addons

    assert addons == expected

def test_get_addons_when_product_created_and_addon_not_created(product_manager, product_data):
    addons = product_manager.create_product(**product_data).get_addons()
    expected = BLANK_PRODUCT.addons

    assert addons == expected

def test_get_addon_when_nothing_created(product_manager):
    addon = product_manager.get_addon()
    assert addon == None

    addon = product_manager.get_addon('RandomID')
    assert addon == None

def test_get_addon_when_product_created_and_addon_created(product_manager, product_data, addon_data):
    addon = product_manager\
            .create_product(**product_data)\
            .create_addon(**addon_data)\
            .get_addon()

    p_id = product_manager.get_product().product.id_
    a_id = product_manager.get_product().id_

    expected = Addon(Product(p_id, **product_data), a_id, **addon_data)
    assert addon == expected

    addon = product_manager.get_addon(a_id)
    assert addon == expected

    addon = product_manager.get_addon('RandomID')
    assert addon == None

def test_get_addon_when_product_not_created_and_addon_created(product_manager, addon_data, a_blank_product):
    addon = product_manager\
            .create_addon(**addon_data)\
            .get_addon()

    id_ = product_manager.get_product().id_

    expected = Addon(a_blank_product, id_, **addon_data)
    assert addon == expected

    addon = product_manager.get_addon(id_)
    assert addon == expected

    addon = product_manager.get_addon('RandomID')
    assert addon == None

def test_get_addon_when_product_created_and_addon_not_created(product_manager, product_data):
    addon = product_manager\
            .create_product(**product_data)\
            .get_addon()

    assert addon == None

    p_id = product_manager.get_product().id_
    addon = product_manager.get_addon(p_id)
    assert addon == None

    addon = product_manager.get_addon('RandomID')
    assert addon == None

def test_remove_addon_when_nothing_created(product_manager):
    product = product_manager.get_product()
    product_manager.remove_addon('RandomID')

    expected = BLANK_PRODUCT
    assert product == BLANK_PRODUCT

def test_remove_addon_when_product_created_and_addon_created(product_manager, product_data, addon_data):
    product = product_manager\
            .create_product(**product_data)\
            .create_addon(**addon_data)\
            .get_product()

    a_id = product.id_
    product = product_manager.remove_addon(a_id).get_product()

    p_id = product.id_

    expected = Product(p_id, **product_data)
    assert product == expected

def test_remove_addon_when_product_created_and_addon_not_created(product_manager, product_data):
    product = product_manager\
            .create_product(**product_data)\
            .get_product()

    product_manager.remove_addon('RandomID')

    assert product == product_manager.get_product()

def test_remove_addon_when_product_not_created_and_addon_created(product_manager, addon_data):
    product = product_manager\
            .create_addon(**addon_data)\
            .get_product()

    id_ = product.id_

    product = product_manager\
            .remove_addon(id_)\
            .get_product()

    expected = BLANK_PRODUCT
    assert product == expected





