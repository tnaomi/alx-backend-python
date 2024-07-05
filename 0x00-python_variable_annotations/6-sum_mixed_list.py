#!/usr/bin/env python3
""" Contains ``sum_mixed_list``"""
from typing import List, Union


def sum_mixed_list(mxd_lst: List[Union[int, float]]) -> float:
    """ Returns the sum of a list of floats and ints

    Args:
        mxd_lst (List[float | int]): _a list of floats and ints_

    Returns:
        float: _sum of all list elements_
    """
    return sum(mxd_lst)
