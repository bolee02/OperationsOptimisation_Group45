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

def transit_coming(x,p_ij,w_ikl) -> np.ndarray:
    """
    Condition to ensure all transit passengers of i travelling to gate k = # of passengers of i travelling
    to K from all other gates
    :param x: numpy array: 1 if aircraft 𝑖 is assigned to gate 𝑘, and 0 otherwise. (decision variable)
    :type x: np.ndarray
    :param y_ijkl: fraction of passengers transiting from a/c i to j via gates k and l
    (of each i, a fraction for each gate) (rows: ac/s, columns: gates
    :type y_ijkl: np.ndarray
    :param e_i: # of passengers in a/c i
    :type e_i: np.ndarray (1D)
    :param p_ij: # of passengers transiting from a/c i to a/c to j
    :type p_ij: np.ndarray
    :return: an array that returns true for each a/c i if condition is made, false otherwise
    """
    #two arrays for boolean checking
    RHS_arr = []
    LHS_arr = []
    for i,ac2gate in enumerate(x):
        for j in x













