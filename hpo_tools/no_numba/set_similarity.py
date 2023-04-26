import numpy as np


def set_sim_max(index1, index2, S):
    S_mini = S[np.ix_(index1, index2)]
    return S_mini.max()


def set_sim_sum(index1, index2, S):
    S_mini = S[np.ix_(index1, index2)]
    return S_mini.sum()


def set_sim_mean(index1, index2, S):
    S_mini = S[np.ix_(index1, index2)]
    return S_mini.mean()


def set_sim_mean_of_sums(index1, index2, S):
    S_mini = S[np.ix_(index1, index2)]
    return 0.5 * (S_mini.max(axis=0).sum() + S_mini.max(axis=1).sum())


def set_sim_funsimavg(index1, index2, S):
    S_mini = S[np.ix_(index1, index2)]
    return 0.5 * (S_mini.max(axis=0).mean() + S_mini.max(axis=1).mean())


def set_sim_max_of_sums(index1, index2, S):
    S_mini = S[np.ix_(index1, index2)]
    return max(S_mini.max(axis=0).sum(), S_mini.max(axis=1).sum())


def set_sim_funsimmax(index1, index2, S):
    S_mini = S[np.ix_(index1, index2)]
    return max(S_mini.max(axis=0).mean(), S_mini.max(axis=1).mean())


def set_sim_bma(index1, index2, S):
    S_mini = S[np.ix_(index1, index2)]
    return (S_mini.max(axis=0).sum() + S_mini.max(axis=1).sum()) / (len(index1) + len(index2))


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
