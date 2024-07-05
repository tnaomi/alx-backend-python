#!/usr/bin/env python3
""" Contains ``make_multiplier``"""
from typing import Callable


def make_multiplier(multiplier: float) -> Callable[[float], float]:
    """ takes a float `multiplier` as argument.
    Returns a function that multiplies a float by `multiplier`.

    Args:
        multiplier (float): _float multiplier_

    Returns:
        Callable[[float], float]: _a function returning float_
    """
    def multiply(a: float) -> float:
        """ Multiply a float by `multiplier`

        Args:
            a (float): _a float number_

        Returns:
            float: _a float product_
        """
        return float(a * multiplier)
    return multiply
