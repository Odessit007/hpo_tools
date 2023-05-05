from multiprocessing import Pool, cpu_count

import numba as nb
import numpy as np
from numpy import single, uint
from numpy.typing import NDArray

from hpo_tools.annotation import Annotation
from hpo_tools.ontology import Ontology
from hpo_tools.with_numba.set_utils import intersection_max, intersection_sum, union_sum


@nb.njit
def sim_resnik(a: int, b: int, ancestors: NDArray[uint], ic: NDArray[single], check_lineage: bool = False):
    A = ancestors[a]
    B = ancestors[b]
    # TODO [V2] Try njit + binary search instead of built-in `in`
    # TODO [V2] Profile function with and without this if for the case when check_lineage=False
    if check_lineage and a not in B and b not in A:
        return 0.0
    return intersection_max(A, B, ic)


@nb.njit
def sim_count(a: int, b: int, ancestors: NDArray[uint], ic: NDArray[single]):
    """Pass ic = np.array([1 for p in graph.nodes], dtype=np.float32)"""
    A = ancestors[a]
    B = ancestors[b]
    return intersection_sum(A, B, ic)


@nb.njit
def sim_graph(a: int, b: int, ancestors: NDArray[uint], ic: NDArray[single]):
    A = ancestors[a]
    B = ancestors[b]
    return intersection_sum(A, B, ic) / union_sum(A, B, ic)


@nb.njit
def sim_lin(a: int, b: int, ancestors: NDArray[uint], ic: NDArray[single]):
    ic_a = ic[a]
    ic_b = ic[b]
    if not ic_a or not ic_b:
        return 0.0
    ic_mica = sim_resnik(a, b, ancestors, ic)
    return 2 * ic_mica / ic_a / ic_b


@nb.njit
def sim_jc(a: int, b: int, ancestors: NDArray[uint], ic: NDArray[single]):
    ic_mica = sim_resnik(a, b, ancestors, ic)
    return 1 - ic[a] - ic[b] + 2 * ic_mica


@nb.njit
def sim_rel(
    a: int,
    b: int,
    ancestors: NDArray[uint],
    ic: NDArray[single],
):
    ic_mica = sim_resnik(a, b, ancestors, ic)
    p_mica = np.exp(-ic_mica)  # IC = -log(P)
    return sim_lin(a, b, ancestors, ic) * (1 - p_mica)


@nb.njit
def sim_info(a: int, b: int, ancestors: NDArray[uint], ic: NDArray[single]):
    ic_mica = sim_resnik(a, b, ancestors, ic)
    return sim_lin(a, b, ancestors, ic) * (1 - 1 / (1 + ic_mica))


# TODO Profile this function when numbers are used instead of strings
@nb.njit
def term_similarity(a: int, b: int, ancestors: NDArray[uint], ic: NDArray[single], similarity: str):
    if similarity == "resnik":
        return sim_resnik(a, b, ancestors, ic)
    if similarity == "count":
        return sim_count(a, b, ancestors, ic)
    if similarity == "graph":
        return sim_graph(a, b, ancestors, ic)
    if similarity == "lin":
        return sim_lin(a, b, ancestors, ic)
    if similarity == "jc":
        return sim_jc(a, b, ancestors, ic)
    if similarity == "rel":
        return sim_rel(a, b, ancestors, ic)
    if similarity == "info":
        return sim_info(a, b, ancestors, ic)


# TODO Profile this function with float32 vs float64
# TODO Port these 2 functions to no-Numba file
@nb.njit
def _sim_term_util(i: int, n: int, ancestors: NDArray[uint], ic: NDArray[single], similarity: str) -> NDArray[single]:
    ans = np.zeros(n, dtype=np.float32)
    for j in range(i + 1, n):
        ans[j] = term_similarity(i, j, ancestors, ic, similarity)
    return ans


def get_term2term_matrix(graph: Ontology, annotation: Annotation, similarity: str, n_processes=-2) -> NDArray[single]:
    if n_processes >= 0:
        n_processes = min(n_processes, cpu_count())
    else:
        n_processes = cpu_count() + n_processes
    n_processes = max(1, n_processes)
    n_nodes = len(graph.nodes)
    ancestors = graph.ancestors
    ic = annotation.ic
    inputs = ((i, n_nodes, ancestors, ic, similarity) for i in range(n_nodes))
    with Pool(n_processes) as pool:
        rows = pool.starmap(_sim_term_util, inputs)
    S = np.vstack(rows)
    S += S.T
    np.fill_diagonal(S, 1.0)
    return S
