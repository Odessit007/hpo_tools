import multiprocessing as mp


def _parse_n_processes(n_processes: int) -> int:
    if n_processes >= 0:
        n_processes = min(n_processes, mp.cpu_count())
    else:
        n_processes = mp.cpu_count() + n_processes
    return max(1, n_processes)


def mp_wrapper(n_processes):
    def decorator(func):
        def wrapper(inputs):
            nonlocal n_processes
            n_processes = _parse_n_processes(n_processes)
            with mp.Pool(n_processes) as p:
                return p.starmap(func, inputs)

        return wrapper

    return decorator
