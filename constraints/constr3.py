import numpy as np
from gurobipy import quicksum


def plane_assigned_to_only_one_gate(x: dict, i: int, K: dict):
    """
    :param x: Gate assignment dict
    :param i: Aircraft index
    :param K: Set of relevant gates
    :return:
    """
    return quicksum(x[i, k] for k in list(K.keys())) == 1

