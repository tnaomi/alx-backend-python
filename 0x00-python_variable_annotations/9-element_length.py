#!/usr/bin/env python3
""" Contains ``make_multiplier``"""
from typing import List, Iterable, Sequence
from typing import Tuple, Mapping, MutableMapping


def element_length(lst: Iterable[Sequence]) -> List[Tuple[Sequence, int]]:
    """ Element length """
    return [(i, len(i)) for i in lst]
