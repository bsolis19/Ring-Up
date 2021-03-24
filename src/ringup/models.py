"""Data models for ringup project"""

import re
import ringup.lib.formula as fi

from ringup.lib.observables import ObservableMixin
from ringup.lib.log import logged

from collections import namedtuple

CustomAttribute = namedtuple('CustomAttribute', ['name', 'value'])


@logged
class Product(ObservableMixin):
    def __init__(
            self,
            id_,
            name,
            cost,
            description='',
            fixedcost=0,
            waste=0.0,
            **extras
            ):
        super().__init__()
        self.id = id_
        self.name = name
        self.cost = cost
        self.description = description
        self.fixedcost = fixedcost
        self.waste = waste

        self._custom_attributes = dict(**extras)

    def calculate_price(self, margin=.75):
        return (self.cost * (1 + self.waste) + self.fixedcost) / (1 - margin)


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
    def fixedcost(self):
        return self._fixedcost

    @fixedcost.setter
    def fixedcost(self, value):
        self._validate_cost(value)
        self._fixedcost = value
        self.changed()

    @property
    def waste(self):
        return self._waste

    @waste.setter
    def waste(self, value):
        if (value > .15):
            raise ValueError("Waste cannot be more than 15%")
        self._waste = float(abs(value))
        self.changed()

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

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self.addonname = value
        self._name = self.product.name + " +" + value

    @property
    def cost(self):
        return self._cost

    @cost.setter
    def cost(self, value):
        self._validate_cost(value)
        self.addoncost = value
        self._cost = round(value + self.product.cost, 2)

    @property
    def fixedcost(self):
        return self.product.fixedcost

    @fixedcost.setter
    def fixedcost(self, value):
        pass

    @property
    def waste(self):
        return self.product.waste

    @waste.setter
    def waste(self, value):
        pass

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = self.product.description +\
            " " + self.product.name + " " + value + " " + self.addonname
        self.addondescription = value


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
