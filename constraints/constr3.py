import numpy as np


def plane_assigned_to_only_one_gate(x, I) -> np.ndarray:
    """
    Condition checks if aircraft is assigned to strictly one gate
    :param x: numpy array: 1 if aircraft 𝑖 is assigned to gate 𝑘, and 0 otherwise.
    :type x: np.ndarray
    :param I: set of all domestic flights
    :type I: np.ndarray
    :return: array which is true if the condition is made, otherwise false
    """
    array = np.array((len(I), 1), dtype=bool)
    for i in range(len(I)):
        array[i] = np.sum(x[:, i], axis=0) == 1

    return array

