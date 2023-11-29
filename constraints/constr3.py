import numpy as np


def plane_assigned_to_only_one_gate(x) -> np.ndarray:
    """
    Condition checks if aircraft is assigned to strictly one gate
    :param x: numpy array: 1 if aircraft 𝑖 is assigned to gate 𝑘, and 0 otherwise.
    :type x: np.ndarray
    :param I: set of all domestic flights
    :type I: np.ndarray
    :return: array which is true if the condition is made, otherwise false
    """
    return np.sum(x, axis=0) == 1

