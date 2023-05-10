import numpy as np


def naive_fitness(x: np.ndarray, rest_code: int, fermata_code: int):
    return np.sum(x)

def continous_fitness(x: np.ndarray, rest_code: int, fermata_code: int):
    rest_cnt = 0
    farmata_cnt = 0
    note_cnt = 0
    for c in x:
        if c == rest_code:
            rest_cnt += 1
        elif c == fermata_code:
            farmata_cnt += 1
        else:
            note_cnt += 1
    return farmata_cnt / len(x)
