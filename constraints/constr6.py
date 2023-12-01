import numpy as np
from gurobipy import Model, GRB, LinExpr, quicksum


def number_of_aircraft_in_the_apron_old(x, K_d, I_d, I_i, K_i):
    NA = find_number_in_apron(K_d, I_d) + find_number_in_apron(K_i, I_i)
    return np.sum(x[len(K_d)+len(K_i)+1, :], axis=0) == NA


def number_of_aircraft_in_the_apron(x, K_d, I_d, I_i, K_i):
    NA = find_number_in_apron(K_d, I_d) + find_number_in_apron(K_i, I_i)
    return (quicksum(x[len(K_d.keys())+len(K_i.keys())+1, i]) for i in range(len(I_d.keys())+len(I_i.keys()))) == NA


def find_number_in_apron(K, I, It):
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

    for i in range(1, I_len+1):  # Arcs from 0th node to all other nodes
        Z[0, i] = model.addVar(lb=0, ub=1, vtype=GRB.BINARY, name=f'x_{0}{i}')
    for i in range(I_len):  # Arcs to |I|th node from all other nodes
        Z[i, I_len] = model.addVar(lb=0, ub=1, vtype=GRB.BINARY, name=f'x_{i}{I_len}')

    for i in range(1, I_len):
        for j in range(1, I_len):
            if not any(all(aircraft in list(It_x.values()) for aircraft in [I[i], I[j]]) for It_x in list(It.values())) and i != j:
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


a = {1: "a", 2: "b", 3: "c"}  # I
b = {1: "a", 2: "b"}  # K
c = {0: a}

print(find_number_in_apron(b, a, c))
