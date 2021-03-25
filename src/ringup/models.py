"""Data models for ringup project"""

import os
import json
import re
import ringup.lib.formula as fi

from ringup.lib.observables import ObservableMixin
from ringup.lib.log import logged


@logged
class Product(ObservableMixin):
    def __init__(
            self,
            sku,
            name,
            cost,
            description='',
            fixed_cost=0,
            waste=0.0,
            **extras
            ):
        super().__init__()
        self.sku = sku
        self.name = name
        self.cost = cost
        self.description = description
        self.fixed_cost = fixed_cost
        self.waste = waste

        self._addons = dict()
        self._custom_attributes = dict(**extras)

    def calculate_price(self, margin=.75):
        return (self.total_cost) / (1 - margin)

    @property
    def total_cost(self):
        return self.calculated_cost + self.fixed_cost

    @property
    def calculated_cost(self):
        return self.cost * (1 + self.waste)

    @property
    def addons(self):
        return self._addons

    def get_addon(self, sku):
        assert self._addons.get(sku, None) == None

    def _register_addon(self, addon):
       self._addons[addon.sku] = addon

    def remove_addon(self, sku):
        del self._addons[sku]

    @property
    def sku(self):
        return self._sku

    @sku.setter
    def sku(self, value):
        if not value:
            raise ValueError('SKU cannot be empty')
        if value and isinstance(value, str):
            self._sku = value
        else:
            raise TypeError('SKU must be a string')

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        try:
            self._name = value.title()
        except AttributeError:
            raise TypeError

    @property
    def cost(self):
        # cost can be a CostFormula instance
        try:
            return self._cost.get_cost()
        except AttributeError:
            return self._cost

    @cost.setter
    def cost(self, value):
        self._validate_cost(value)
        self._cost = value

    @property
    def fixed_cost(self):
        return self._fixed_cost

    @fixed_cost.setter
    def fixed_cost(self, value):
        self._validate_cost(value)
        self._fixed_cost = value
        self.changed()

    @property
    def waste(self):
        return self._waste

    @waste.setter
    def waste(self, value):
        self._validate_waste(value)
        self._waste = float(abs(value))
        self.changed()

    def _validate_waste(self, waste):
        if (waste > .15):
            raise ValueError("Waste cannot be more than 15%")

    @property
    def custom_attributes(self):
        return self._custom_attributes

    def set_custom_attribute(self, name, value):
        self._custom_attributes[name] = value

    def get_custom_attribute(self, name):
        return self._custom_attributes[name]

    def _validate_cost(self, cost):
        if (cost < 0):
            raise ValueError("Expected nonnegative cost")

    def __str__(self):
        return self.name

    def __repr__(self):
        return "{__class__.__name__}({_args_str})".format(
                __class__=self.__class__,
                _args_str=", ".join(
                    "=".join(
                        (str(key), repr(val))
                        ) for key, val in vars(self).items()
                    )
                )

    def __eq__(self, other):
        return vars(self) == vars(other)

    __hash__ = None

    price = property(calculate_price)


@logged
class Addon(Product):
    def __init__(self, product, *args, **extras):
        self.product = product
        super().__init__(*args, **extras)
        self._register_addon(self)

    @property
    def addons(self):
        return self.product.addons

    def get_addon(self, sku):
        if self.sku == sku:
            return self
        return self.product.get_addon(sku)

    def _register_addon(self, addon):
       self.product._register_addon(addon)

    def remove_addon(self, sku):
        self.product.remove_addon(sku)
        if self.product.sku == sku:
            self.product = self.product.product
        elif self.sku == sku:
            raise ValueError("Cannot remove head object from chain of references")

    @property
    def calculated_cost(self):
        return super().calculated_cost + self.product.calculated_cost

    @property
    def total_cost(self):
        return self.calculated_cost + self.product.fixed_cost

    @property
    def fixed_cost(self):
        return self.product.fixed_cost

    @fixed_cost.setter
    def fixed_cost(self, value):
        if value != 0:
            raise ValueError("Addon.fixed_cost must be zero")
        self._fixed_cost = value

class SettingsModel:
    """A model for saving settings"""

    variables = {
            'font size': {
                'type': 'int',
                'value': 9,
            },
        }

    def __init__(self, filename='ringup_settings.json', path='~'):
        # determine file path
        self.filepath = os.path.join(os.path.expanduser(path), filename)

        # load in saved values
        self.load()

    def set(self, key, value):
        """Set a variable value"""
        if (
            key in self.variables and
            type(value).__name__==self.variables[key]['type']
        ):
            self.variables[key]['value'] = value
        else:
            raise ValueError('Bad key or wrong variable type')

    def save(self, settings=None):
        """Save current settings to file."""
        json_string=json.dumps(self.variables)
        with open(self.filepath, 'w', encoding='utf-8') as fh:
            fh.write(json_string)

    def load(self):
        """Load settings from file."""

        # if file doesn't exist, return
        if not os.path.exists(self.filepath):
            return

        # open file and read raw values
        with open(self.filepath, 'r', encoding='utf-8') as fh:
            raw_values = json.loads(fh.read())

        # don't implicitly trust raw  values, get only known keys
        for key in self.variables:
            if key in raw_values and 'value' in raw_values[key]:
                raw_value = raw_values[key]['value']
                self.variables[key]['value'] = raw_value

@logged
class CostFormula:
    def __init__(self, formula, variables):
        self.variables = variables
        self.formula = formula

        self.logger.debug("[init] formula {0}, variables {1}".format(
                formula,
                variables,
            )
        )

    @property
    def formula(self):
        return self._formula

    @formula.setter
    def formula(self, value):
        self._validate_formula(CostFormula._get_hard(value, self.variables))
        self._formula = value

    def get_cost(self):
        hard = CostFormula._get_hard(self.formula, self.variables)
        fi.parse(hard)
        self.logger.debug('[get_cost] parsed {0} ({1}) -> {2}'.format(
                self.formula,
                hard,
                fi.value,
            )
        )
        return fi.value

    @staticmethod
    def _get_hard(formula, variables):
        s = formula
        for x in variables:
            s = re.sub(x, str(variables[x]), s)
        return s

    def _validate_formula(self, str_):
        fi.parse(str_)

    def __lt__(self, other):
        return self.get_cost() < other

    def __gt__(self, other):
        return self.get_cost() > other
