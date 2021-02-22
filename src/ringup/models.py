"""Data models for ringup project"""

import re

from collections import namedtuple

CustomAttribute = namedtuple('CustomAttribute', ['name', 'value'])

class Product:
    def __init__(self, title, cost, description='', costformula='', **extras):
        self.title = title
        self.cost = cost
        self.description = description
        self.costformula = costformula
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
        return self._cost

    @cost.setter
    def cost(self, value):
        self._validate_cost(value)
        self._cost = value

    @property
    def costformula(self):
        return self._costformula

    @costformula.setter
    def costformula(self, value):
        self._costformula = value
        self._cost = value.simplify()

    def _validate_cost(self, cost):
        if (cost < 0):
            raise ValueError("Expected nonnegative cost")

    def __str__(self):
        return self.title

    def __repr__(self):
        return "{__class__.__name__}({_args_str})".format(
                __class__ = self.__class__,
                _args_str = ", ".join(
                    "=".join(
                        (str(key), repr(val))
                        ) for key, val in vars(self).items()
                    )
                )
    def __eq__(self, other):
        return vars(self) == vars(other)

    __hash__ = None

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
        self._description = self.product.description + " " + self.product.title + " " + value + " " + self.addontitle
        self.addondescription = value

class CostFormula:
    def __init__(self, formula_str, attr_dict):
        self.formula_str = formula_str
        self.attr_dict = attr_dict

    @property
    def formula_str(self):
        return self._formula_str

    @formula_str.setter
    def formula_str(self, value):
        self._validate_formula(value)
        self._formula_str = value

    def simplify(self):
        mapped = ''
        for attr in self.attr_dict:
            mapped = re.sub(attr, str(self.attr_dict[attr]), self.formula_str)

        return eval(mapped)

    def _validate_formula(self, str_):
        pass

class BinaryOp:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return self.op_str + '(' + str(self.left) + ',' + str(self.right) + ')'

class Sum(BinaryOp):
    op_str = 'Sum'

    def evaluate(self):
        return self.left.evaluate() + self.right.evaluate()

class Prod(BinaryOp):
    op_str = 'Prod'

   def evaluate(self):
       return self.left.evaluate() * self.right.evaluate()

class Quot(BinaryOp):
    op_str = 'Quot'

    def evaluate(self):
        return self.left.evauate() / self.right.evaluate()

    @property
    def right(self):
        return self._right

    @right.setter(self, value):
        if value.evaluate() != 0:
            self.right = value
        else:
            raise ValueError("Operand 2 cannot be '0' for " + str(self))

class Diff(BinaryOp):
    op_str = 'Diff'

    def evaluate(self):
        return self.left.evaulate() - self.right.evaluate()

class Number:
    def __init__(self,value):
        self.value = value

    def __str__(self):
        return 'Num(' + str(self.value) + ')'

class Variable:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return 'Var(' + self.name + ')'





