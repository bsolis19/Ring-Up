"""Test the product driver."""
from ringup.product import Driver
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


@pytest.fixture()
def product_data():
    return product_data_set


@pytest.fixture()
def addon_data():
    return addon_data_set

@pytest.fixture()
def driver():
    return Driver()

def test_create_product(driver, product_data):
    product = driver.create_product(**product_data).get_product()
    for key, val in product_data.items():
        assert getattr(product, key) == val

def test_create_addon(driver, addon_data):
    addon = driver.create_addon(**addon_data).get_addon()
    for key, val in addon_data.items():
        assert getattr(addon, key) == val

def test_get_product_when_product_not_created(driver):
    product = driver.get_product()
    assert product == BLANK_PRODUCT

def test_get_product_when_product_created(driver, product_data):
    product = driver.create_product(**product_data).get_product()

    for key, val in product_data.items():
        assert getattr(product, key) == val











