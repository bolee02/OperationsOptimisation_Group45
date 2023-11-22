import numpy as np


def gate_assigned_to_only_one_gate(x, I):
    """
    :param x: numpy array: 1 if aircraft 𝑖 is assigned to gate 𝑘, and 0 otherwise.
    :type x:
    :param I:
    :return:
    """
    array = np.array((len(I), 1), dtype=bool)
    for i in range(len(I)):
        array[i] = sum(x[i]) == 1

    return array

