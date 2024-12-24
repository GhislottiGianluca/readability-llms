from typing import List, Tuple

import numpy as np
import scipy.stats as stats
import math


def wilcoxon_test(a: List[float], b: List[float]) -> Tuple[float, float]:
    assert len(a) == len(b), "The two list must be of the same length: {}, {}".format(
        len(a), len(b)
    )
    return stats.wilcoxon(a, b)


def mannwhitney_test(a: List[float], b: List[float]) -> Tuple[float, float]:
    if np.array_equal(a, b):
        # mannwhitneyu throws a value error when two arrays are equal
        return math.inf, math.inf
    return stats.mannwhitneyu(a, b)


def summary(a: List[float]) -> str:
    array = np.asarray(a)

    if min(array) == max(array) and min(array) == 0.0:
        return f"Mean: {0.0}, Median: {0.0}, Std: {0.0}, Min: {0.0}, Max: {0.0}"
    return f"Mean: {np.mean(array)}, Median: {np.median(array)}, Std: {np.std(array)}, Min: {np.min(array)}, Max: {np.max(array)}"
