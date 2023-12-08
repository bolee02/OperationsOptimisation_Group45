import numpy as np
from gurobipy import quicksum

def transit_leaving(x: dict, p_ij: dict, w_ikl: dict, i: int) -> np.ndarray:
    """
    Condition to ensure all transit passengers of aircraft i travel from assigned gate k to other gates
    :param x: numpy array: 1 if aircraft 𝑖 is assigned to gate 𝑘, and 0 otherwise. (decision variable)
    :param p_ij: # of passengers transiting from a/c i to a/c to j
    :param w_ikl: # of passengers of a/c i travelling from gate k to gate l
    :param i: Aircraft index
    :return: an array that returns true for each a/c i if condition is made, false otherwise
    """
    #find the assigned gate of a/c i
    k = list(x[i].keys())[list(x[i].values()).index(1)]
    #total passengers transiting from a/c i (RIGHT HAND SIDE)
    RHS = quicksum([p_ij[i, j] for j in list(x.keys())]) * x[i, k]
    #passengers of a/c i travelling from gate k to other gates (LEFT HAND SIDE)
    LHS = quicksum(w_ikl[i, k, l] for l in list(x[0].keys()))
    return LHS == RHS


def transit_coming(x: dict, p_ij: dict, w_ikl: dict, i: int) -> np.ndarray:
    """
    Condition to ensure all transit passengers of aircraft i travel from assigned gate k to other gates
    :param x: numpy array: 1 if aircraft 𝑖 is assigned to gate 𝑘, and 0 otherwise. (decision variable)
    :param p_ij: # of passengers transiting from a/c i to a/c to j
    :param w_ikl: # of passengers of a/c i travelling from gate k to gate l
    :param i: Aircraft index
    :return: an array that returns true for each a/c i if condition is made, false otherwise
    """
    #find the assigned gate of a/c i
    k = list(x[i].keys())[list(x[i].values()).index(1)]
    RHS = quicksum([p_ij[i, j] * x[j, k] for j in list(x.keys())])
    LHS = quicksum(w_ikl[i, l, k] for l in list(x[0].keys()))
    return LHS == RHS













