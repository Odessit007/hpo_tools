from multiprocessing import Pool, cpu_count

import numba as nb
import numpy as np
from numpy import single, uint
from numpy.typing import NDArray


@nb.njit
def get_row_max(row_index, col_index, matrix):
    ans = np.zeros(len(row_index), dtype=matrix.dtype)
    for i, ix in enumerate(row_index):
        for jx in col_index:
            ans[i] = max(ans[i], matrix[ix][jx])
    return ans


@nb.njit
def set_sim_max(index1, index2, S):
    ans = 0.0
    for ix in index1:
        for jx in index2:
            ans = max(ans, S[ix][jx])
    return ans


@nb.njit
def set_sim_sum(index1, index2, S):
    ans = 0.0
    for ix in index1:
        for jx in index2:
            ans += S[ix][jx]
    return ans


@nb.njit
def set_sim_mean(index1, index2, S):
    return set_sim_sum(index2, index2, S) / (len(index1) * len(index2))


@nb.njit
def set_sim_mean_of_sums(index1, index2, S):
    row_max = get_row_max(index1, index2, S)
    col_max = get_row_max(index2, index1, S.T)
    return 0.5 * (row_max.sum() + col_max.sum())


@nb.njit
def set_sim_funsimavg(index1, index2, S):
    row_max = get_row_max(index1, index2, S)
    col_max = get_row_max(index2, index1, S.T)
    return 0.5 * (row_max.mean() + col_max.mean())


@nb.njit
def set_sim_max_of_sums(index1, index2, S):
    row_max = get_row_max(index1, index2, S)
    col_max = get_row_max(index2, index1, S.T)
    return max(row_max.sum(), col_max.sum())


@nb.njit
def set_sim_funsimmax(index1, index2, S):
    row_max = get_row_max(index1, index2, S)
    col_max = get_row_max(index2, index1, S.T)
    return max(row_max.mean(), col_max.mean())


@nb.njit
def set_sim_bma(index1, index2, S):
    row_max = get_row_max(index1, index2, S)
    col_max = get_row_max(index2, index1, S.T)
    return (row_max.sum() + col_max.sum()) / (len(index1) + len(index2))


set_similarities = {
    "max": set_sim_max,
    "sum": set_sim_sum,
    "mean": set_sim_mean,
    "mean_of_sums": set_sim_mean_of_sums,
    "funsimavg": set_sim_funsimavg,
    "max_of_sums": set_sim_max_of_sums,
    "funsimmax": set_sim_funsimmax,
    "bma": set_sim_bma,
}


@nb.njit
def set_similarity(index1: NDArray[uint], index2: NDArray[uint], S: NDArray[single], similarity: str):
    if similarity == "max":
        return set_sim_max(index1, index2, S)
    if similarity == "sum":
        return set_sim_sum(index1, index2, S)
    if similarity == "mean":
        return set_sim_mean(index1, index2, S)
    if similarity == "mean_of_sums":
        return set_sim_mean_of_sums(index1, index2, S)
    if similarity == "funsimavg":
        return set_sim_funsimavg(index1, index2, S)
    if similarity == "max_of_sums":
        return set_sim_max_of_sums(index1, index2, S)
    if similarity == "funsimmax":
        return set_sim_funsimmax(index1, index2, S)
    if similarity == "bma":
        return set_sim_bma(index1, index2, S)


# TODO Port these 2 functions to no-Numba file
@nb.njit
def _sim_set_util(index1: uint, indexes2: NDArray[uint], S: NDArray[single], similarity: str) -> NDArray[single]:
    n = len(indexes2)
    ans = np.zeros(n, dtype=single)
    for j, index2 in enumerate(indexes2):
        ans[j] = set_similarity(index1, index2, S, similarity)
    return ans


def get_set2set_matrix(
    indexes1: NDArray[uint], indexes2: NDArray[uint], S: NDArray[single], similarity: str, n_processes=-2
) -> NDArray[single]:
    if n_processes >= 0:
        n_processes = min(n_processes, cpu_count())
    else:
        n_processes = cpu_count() + n_processes
    n_processes = max(1, n_processes)
    inputs = ((index, indexes2, S, similarity) for index in indexes1)
    with Pool(n_processes) as pool:
        rows = pool.starmap(_sim_set_util, inputs)
    return np.vstack(rows)
