import numpy as np
from gurobipy import Model, GRB, LinExpr, quicksum


def number_of_aircraft_in_the_apron(x, K, I):
    return np.sum(x[len(K)+1, :], axis=0) == find_number_in_apron(K, I)


def find_number_in_apron(K, I):
    '''
    :param K:
    :type K: dict
    :param I:
    :type I: dict
    :return:
    '''
    I_len = len(I.keys()) + 1
    K_len = len(K.keys()) - 1

    model = Model()
    Z = {}

    for i in range(I_len):
        for j in range(I_len):
            Z[i, j] = model.addVar(lb=0, ub=1, vtype=GRB.BINARY, name=f'x_{i}{j}')

    model.update()

    C1 = model.addConstrs((quicksum(Z[0, j] for j in range(I_len)) <= K_len), name="C1")
    C2 = model.addConstrs((quicksum(Z[i, I_len] for i in range(I_len)) <= K_len), name="C2")
    C3 = model.addConstrs(((quicksum(Z[i, j]) == quicksum(Z[j, i]) for j in range(I_len)) for i in range(I_len)), name="C3")
    C4 = model.addConstrs(((quicksum(Z[i, j]) for j in range(I_len)) for i in range(I_len)), name="C4")

    obj = LinExpr()
    for i in range(I_len):
        for j in range(I_len):
            obj += Z[i, j]

    model.setObjective(obj, GRB.MAXIMIZE)
    model.update()
    model.optimize()
    return I_len - 1 - Model.getObjective().getValue()