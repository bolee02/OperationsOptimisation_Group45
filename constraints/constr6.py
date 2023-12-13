import numpy as np
from gurobipy import Model, GRB, LinExpr, quicksum


def number_of_aircraft_in_the_apron(x: dict, K: dict, I: dict, NA: int):
    """
    :param x: Gate assignment dict
    :param K_d: Set of all domestic gates
    :param I_d: Set of all domestic aircraft
    :param I_D_t: Set of all domestic overlapping aircraft
    :param K_i: Set of all international gates
    :param I_i: Set of all international aircraft
    :param I_I_t: Set of all international overlapping aircraft
    :return:
    """
    return (quicksum(x[len(K)+1, i]) for i in range(len(I)) == NA)


def find_number_in_apron(K: dict, I: dict, It: dict):
    """
    :param K: Set of gates
    :param I: Set of aircraft
    :param It: Set of overlapping aircraft
    :return:
    """
    I_len = len(I.keys()) + 1
    K_len = len(K.keys()) - 1

    model = Model()
    Z = {}

    for i in range(1, I_len+1):  # Arcs from 0th node to all other nodes
        Z[0, i] = model.addVar(lb=0, ub=1, vtype=GRB.BINARY, name=f'x_{0}{i}')
    for i in range(I_len):  # Arcs to |I|th node from all other nodes
        Z[i, I_len] = model.addVar(lb=0, ub=1, vtype=GRB.BINARY, name=f'x_{i}{I_len}')

    for i in range(1, I_len):
        for j in range(1, I_len):
            # if aircraft i and j are in all present in any instance It_x of the overlapping set I_t and i is not j
            # create a link between the aircraft
            if not any(all(aircraft in list(It_x.keys()) for aircraft in [i, j]) for It_x in list(It.values())) and i != j:
                Z[i, j] = model.addVar(lb=0, ub=1, vtype=GRB.BINARY, name=f'x_{i}{j}')
            else:
                Z[i, j] = 0

    model.update()
    C1 = model.addConstr((quicksum(Z[0, j] for j in range(1, I_len+1)) <= K_len), name="C1")
    C2 = model.addConstr((quicksum(Z[i, I_len] for i in range(I_len)) <= K_len), name="C2")

    for i in range(I_len):
        C3 = model.addConstr((quicksum(Z[i, j] for j in range(1, I_len+1)) == quicksum(Z[j, i+1] for j in range(I_len))), name=f"C{3+i}")
    for i in range(I_len):
        C4 = model.addConstr((quicksum(Z[i, j] for j in range(1, I_len+1)) <= 1), name=f"C{3+I_len+1}")

    obj = LinExpr()
    for i in range(I_len):
        for j in range(1, I_len+1):
            obj += Z[i, j]

    model.setObjective(obj, GRB.MAXIMIZE)
    model.update()
    model.optimize()
    return I_len - 1 - model.ObjVal
