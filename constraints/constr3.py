import numpy as np
from gurobipy import quicksum


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


def plane_assigned_to_only_one_gate_dict(x, K_i, K_d):
    return (quicksum(x[:, k]) for k in range(len(K_d.keys())+len(K_i.keys())))

