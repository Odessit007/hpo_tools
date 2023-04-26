from typing import Set

import numpy as np
from numpy.typing import NDArray


def intersection_sum(A: Set[int], B: Set[int], IC: NDArray[np.float32]) -> np.float32:
    """
    :param A: set of nonnegative integers
    :param B: set of nonnegative integers
    :param IC: 1-d Numpy array of nonnegative integers, values in A and B are treated as indexes for array IC
    """
    return sum(IC[x] for x in (A & B))


def union_sum(A: Set[int], B: Set[int], IC: NDArray[np.float32]) -> np.float32:
    """
    :param A: set of nonnegative integers
    :param B: set of nonnegative integers
    :param IC: 1-d Numpy array of nonnegative integers, values in A and B are treated as indexes for array IC
    """
    return sum(IC[x] for x in (A | B))


def set_sum(A: Set[int], IC: NDArray[np.float32]) -> np.float32:
    """
    :param A: set of nonnegative integers, must be sorted in increasing order
    :param IC: 1-d Numpy array of nonnegative integers, values in A and B are treated as indexes for array IC
    """
    return sum(IC[x] for x in A)
