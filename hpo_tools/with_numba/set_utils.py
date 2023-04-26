import numba as nb
from numpy.typing import NDArray


@nb.njit
def intersection_max(A: NDArray, B: NDArray, IC: NDArray) -> float:
    """
    :param A: A 1-d Numpy array of nonnegative integers, must be sorted in increasing order
    :param B: A 1-d Numpy array of nonnegative integers, must be sorted in increasing order
    :param IC: A 1-d Numpy array of nonnegative integers, values in A and B are treated as indexes for array IC
    :return: max(IC[x] for x in (A & B)) but easily usable by Numba
    """
    i_a, i_b = 0, 0
    n_a, n_b = len(A), len(B)
    ans = 0.0
    while i_a < n_a and i_b < n_b:
        a_val, b_val = A[i_a], B[i_b]
        if a_val == b_val:
            ans = max(ans, IC[a_val])
            i_a += 1
            i_b += 1
        elif a_val < b_val:
            i_a += 1
        else:
            i_b += 1
    return ans


@nb.njit
def intersection_sum(A: NDArray, B: NDArray, IC: NDArray) -> float:
    """
    :param A: A 1-d Numpy array of nonnegative integers, must be sorted in increasing order
    :param B: A 1-d Numpy array of nonnegative integers, must be sorted in increasing order
    :param IC: A 1-d Numpy array of nonnegative integers, values in A and B are treated as indexes for array IC
    :return: sum(IC[x] for x in (A & B)) but easily usable by Numba
    """
    i_a, i_b = 0, 0
    n_a, n_b = len(A), len(B)
    ans = 0.0
    while i_a < n_a and i_b < n_b:
        a_val, b_val = A[i_a], B[i_b]
        if a_val == b_val:
            ans += IC[a_val]
            i_a += 1
            i_b += 1
        elif a_val < b_val:
            i_a += 1
        else:
            i_b += 1
    return ans


@nb.njit
def union_sum(A: NDArray, B: NDArray, IC: NDArray) -> float:
    """
    :param A: A 1-d Numpy array of nonnegative integers, must be sorted in increasing order
    :param B: A 1-d Numpy array of nonnegative integers, must be sorted in increasing order
    :param IC: A 1-d Numpy array of nonnegative integers, values in A and B are treated as indexes for array IC
    :return: sum(IC[x] for x in (A | B)) but easily usable by Numba
    """
    prev_val = -1
    i_a, i_b = 0, 0
    n_a, n_b = len(A), len(B)
    ans = 0.0
    while i_a < n_a and i_b < n_b:
        a_val, b_val = A[i_a], B[i_b]
        if a_val == b_val:
            if a_val != prev_val:
                ans += IC[a_val]
            i_a += 1
            i_b += 1
        elif a_val < b_val:
            ans += IC[a_val]
            i_a += 1
        else:
            ans += IC[b_val]
            i_b += 1
    while i_a < n_a:
        ans += IC[A[i_a]]
        i_a += 1
    while i_b < n_b:
        ans += IC[B[i_b]]
        i_b += 1
    return ans


@nb.njit
def union_sum_2(A: NDArray, B: NDArray, IC: NDArray) -> float:
    """
    :param A: A 1-d Numpy array of nonnegative integers, must be sorted in increasing order
    :param B: A 1-d Numpy array of nonnegative integers, must be sorted in increasing order
    :param IC: A 1-d Numpy array of nonnegative integers, values in A and B are treated as indexes for array IC
    :return: sum(IC[x] for x in (A | B)) but easily usable by Numba
    """
    sum_intersection = intersection_sum(A, B, IC)
    sum_a, sum_b = 0.0, 0.0
    for a in A:
        sum_a += IC[a]
    for b in B:
        sum_b += IC[b]
    return sum_a + sum_b - sum_intersection


@nb.njit
def set_sum(A, IC):
    """
    :param A: A 1-d Numpy array of nonnegative integers, must be sorted in increasing order
    :param IC: A 1-d Numpy array of nonnegative integers, values in A and B are treated as indexes for array IC
    :return: sum(IC[x] for x in A) but easily usable by Numba
    """
    ans = 0.0
    for a in A:
        ans += IC[a]
    return ans
