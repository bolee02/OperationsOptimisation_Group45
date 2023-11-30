import numpy as np
from gurobipy import Model, GRB, LinExpr, quicksum


def number_of_aircraft_in_the_apron_old(x, K_d, I_d, I_i, K_i):
    NA = find_number_in_apron(K_d, I_d) + find_number_in_apron(K_i, I_i)
    return np.sum(x[len(K_d)+len(K_i)+1, :], axis=0) == NA


def number_of_aircraft_in_the_apron(x, K_d, I_d, I_i, K_i):
    NA = find_number_in_apron(K_d, I_d) + find_number_in_apron(K_i, I_i)
    return (quicksum(x[len(K_d.keys())+len(K_i.keys())+1, i]) for i in range(len(I_d.keys())+len(I_i.keys()))) == NA


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
    A = (quicksum(Z[0, j] for j in range(I_len)) <= K_len)
    C1 = model.addConstr((quicksum(Z[0, j] for j in range(I_len)) <= K_len), name="C1")
    B = (quicksum(Z[i, I_len-1] for i in range(I_len)) <= K_len)
    C2 = model.addConstr((quicksum(Z[i, I_len-1] for i in range(I_len)) <= K_len), name="C2")
    C = (quicksum(Z[i, j]) == quicksum(Z[j, i]) for j in range(I_len`) for i in range(I_len))
    C3 = model.addConstr((quicksum(Z[i, :]) == quicksum(Z[:, i]) for i in range(I_len)), name="C3")
    D = ((quicksum(Z[i, j]) for j in range(I_len)) for i in range(I_len))
    C4 = model.addConstr(((quicksum(Z[i, j]) for j in range(I_len)) for i in range(I_len)), name="C4")

    obj = LinExpr()
    for i in range(I_len):
        for j in range(I_len):
            obj += Z[i, j]

    model.setObjective(obj, GRB.MAXIMIZE)
    model.update()
    model.optimize()
    return I_len - 1 - Model.getObjective().getValue()


a = {1: "a", 2: "b", 3: "c"}  # I
b = {1: "a", 2: "b"}  # K

print(find_number_in_apron(b, a))