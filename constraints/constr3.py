import numpy as np
from gurobipy import quicksum


def plane_assigned_to_only_one_gate_dict(x, i, K):
    return quicksum(x[i, k] for k in range(K)) == 1

