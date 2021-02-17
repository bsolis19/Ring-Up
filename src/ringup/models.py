"""Data models for ringup project"""

import os
import json

from collections import namedtuple

CustomAttribute = namedtuple('CustomAttribute', ['name', 'value'])

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
