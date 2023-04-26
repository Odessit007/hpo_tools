from collections.abc import Sequence
from typing import Set

import numpy as np
from numpy import single
from numpy.typing import NDArray


def _ic_sum(A: Set[int], ic: NDArray[single]):
    s = 0.0
    for x in A:
        s += ic[x]
    return s


# Term-to-term similarities
def sim_resnik(a: int, b: int, ancestors: Sequence[Set[int]], ic: NDArray[single], check_lineage: bool = False):
    A = ancestors[a]
    B = ancestors[b]
    if check_lineage and a not in B and b not in A:
        return 0.0
    A_and_B = A & B
    max_ = 0.0
    for x in A_and_B:
        max_ = max(max_, ic[x])
    return max_


def sim_count(
    a: int,
    b: int,
    ancestors: Sequence[Set[int]],
    ic: NDArray[single],
):
    A = ancestors[a]
    B = ancestors[b]
    return len(A & B)


def sim_graph(
    a: int,
    b: int,
    ancestors: Sequence[Set[int]],
    ic: NDArray[single],
):
    A = ancestors[a]
    B = ancestors[b]
    A_and_B = A & B
    A_or_B = A | B
    return _ic_sum(A_and_B, ic) / _ic_sum(A_or_B, ic)


def sim_lin(
    a: int,
    b: int,
    ancestors: Sequence[Set[int]],
    ic: NDArray[single],
):
    ic_a = ic[a]
    ic_b = ic[b]
    if not ic_a or not ic_b:
        return 0.0
    ic_mica = sim_resnik(a, b, ancestors, ic)
    return 2 * ic_mica / ic_a / ic_b


def sim_jc(
    a: int,
    b: int,
    ancestors: Sequence[Set[int]],
    ic: NDArray[single],
):
    ic_mica = sim_resnik(a, b, ancestors, ic)
    return 1 - ic[a] - ic[b] + 2 * ic_mica


def sim_rel(
    a: int,
    b: int,
    ancestors: Sequence[Set[int]],
    ic: NDArray[single],
):
    ic_mica = sim_resnik(a, b, ancestors, ic)
    p_mica = np.exp(-ic_mica)  # IC = -log(P)
    return sim_lin(a, b, ancestors, ic) * (1 - p_mica)


def sim_info(
    a: int,
    b: int,
    ancestors: Sequence[Set[int]],
    ic: NDArray[single],
):
    ic_mica = sim_resnik(a, b, ancestors, ic)
    return sim_lin(a, b, ancestors, ic) * (1 - 1 / (1 + ic_mica))
