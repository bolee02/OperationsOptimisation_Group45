import numpy as np
from gurobipy import quicksum


def transit_leaving(x: dict, K: dict, I: dict, p: dict, w: dict, i: int, k: str) -> np.ndarray:
    """
    Condition to ensure all transit passengers of aircraft i travel from assigned gate k to other gates
    :param x: numpy array: 1 if aircraft 𝑖 is assigned to gate 𝑘, and 0 otherwise. (decision variable)
    :param K: Set of all gates
    :param I: Set of all flights
    :param p: Set containing # of passengers transiting from a/c i to a/c to j
    :param w: Set containing # of passengers of a/c i travelling from gate k to gate l
    :param i: Aircraft index
    :param k: Gate index
    :return: linvar object contain the constraint
    """

    """ removed because the type contained in x is an instance of gurobipy.Var which I believe does not have a value 
        in python itself. (I believe. I'm not sure though will be checking further) """
    # find the assigned gate of a/c i
    # k = list(x[i].keys())[list(x[i].values()).index(1)]

    # total passengers transiting from a/c i (RIGHT HAND SIDE)
    RHS = quicksum([p[i][j] for j in list(I.keys())]) * x[i, k]
    # passengers of a/c i travelling from gate k to other gates (LEFT HAND SIDE)
    LHS = quicksum(w[i, k, l] for l in list(K.keys()))
    return LHS == RHS


def transit_coming(x: dict, K_gi: dict, I: dict, p: dict, w: dict, i: int, k: str) -> np.ndarray:
    """
    Condition to ensure all transit passengers of aircraft i travel from assigned gate k to other gates
    :param x: numpy array: 1 if aircraft 𝑖 is assigned to gate 𝑘, and 0 otherwise. (decision variable)
    :param K_gi: Set of relevant gates
    :param I: Set of all flights
    :param p: Set containing # of passengers transiting from a/c i to a/c to j
    :param w: Set containing # of passengers of a/c i travelling from gate k to gate l
    :param i: Aircraft index
    :param k: Gate index
    :return: linvar object contain the constraint
    """

    """ removed because the type contained in x is an instance of gurobipy.Var which I believe does not have a value 
        in python itself. (I believe. I'm not sure though will be checking further) """
    # find the assigned gate of a/c i
    # k = list(x[i].keys())[list(x[i].values()).index(1)]
    RHS = quicksum([p[i][j] * x[j, k] for j in list(I.keys())])
    LHS = quicksum(w[i, l, k] for l in list(K_gi.keys()))
    return LHS == RHS













