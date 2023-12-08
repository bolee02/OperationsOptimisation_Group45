import numpy as np
from gurobipy import quicksum


def plane_assigned_to_only_one_gate_dict(x: dict, i: int, K: dict):
    """
    :param x: Gate assignment dict
    :param i: Aircraft index
    :param K: Set of all gates
    :return:
    """
    return quicksum(x[i, k] for k in range(len(K.keys()))) == 1

