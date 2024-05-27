import numpy as np
from fl.types import List, Matrix, Vector


def aggregator_mean(weights_list: List[List[Matrix[np.float_]]]) -> Vector[Matrix[np.float_]]:
    """
    WARNING! The weights list is transformed into a Numpy array of Numpy arrays.
    :param weights_list:
    :return:
    """
    result = []
    for j in range(len(weights_list[0])):
        result.append(np.mean([c[j] for c in weights_list], axis=0))
    return np.array(result, dtype="object")


def aggregator_median(weights_list: List[List[Matrix[np.float_]]]) -> Vector[Matrix[np.float_]]:
    """
    WARNING! The weights list is transformed into a Numpy array of Numpy arrays.
    :param weights_list:
    :return:
    """
    result = []
    for j in range(len(weights_list[0])):
        result.append(np.median([c[j] for c in weights_list], axis=0))
    return np.array(result, dtype="object")
