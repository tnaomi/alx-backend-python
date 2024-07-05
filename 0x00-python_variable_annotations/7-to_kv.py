#!/usr/bin/env python3
""" Contains ``to_kv``"""
from typing import Tuple, Union


def to_kv(k: str, v: Union[int, float]) -> Tuple[str, float]:
    """ takes a string `k` and an int OR float `v` as arguments.
    Returns a tuple

    Args:
        k (str): _description_
        v (Union[int, float]): _description_

    Returns:
        Tuple[str, float]: _description_
    """
    return (k, v**2)
