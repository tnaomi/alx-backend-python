#!/usr/bin/env python3
""" Contains `sum_list`"""
from typing import List


def sum_list(input_list: List[float]) -> float:
    """ Returns the sum of a list of floats

    Args:
        input_list (List[float]): _a list of floats_

    Returns:
        float: _sum of all list elements_
    """
    return sum(input_list)
