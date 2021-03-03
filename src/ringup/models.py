"""Data models for ringup project"""

import re
import ringup.lib.formula as fi


from ringup.lib.log import logged

from collections import namedtuple

CustomAttribute = namedtuple('CustomAttribute', ['name', 'value'])


@logged
class Product:
    def __init__(self, title, cost, description='', **extras):
        self.title = title
        self.cost = cost
        self.description = description
        self.__dict__.update(extras)

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        try:
            self._title = value.title()
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

    def _validate_cost(self, cost):
        if (cost < 0):
            raise ValueError("Expected nonnegative cost")

    def __str__(self):
        return self.title

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


@logged
class Addon(Product):
    def __init__(self, product, *args, **extras):
        self.product = product
        super().__init__(*args, **extras)

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self.addontitle = value
        self._title = self.product.title + " +" + value

    @property
    def cost(self):
        return self._cost

    @cost.setter
    def cost(self, value):
        self._validate_cost(value)
        self.addoncost = value
        self._cost = round(value + self.product.cost, 2)

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = self.product.description +\
            " " + self.product.title + " " + value + " " + self.addontitle
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
