import numpy as np
from gurobipy import Model, GRB, LinExpr, quicksum


def number_of_aircraft_in_the_apron(x: dict, K: dict, I: dict, NA: int) -> LinExpr:
    """
    :param x: Gate assignment dict
    :param K: Set of all gates
    :param I: Set of all aircaft
    :param NA: Apron number
    :return: LinExpr instance of the constraint
    """
    return quicksum(x[i, "a"] for i in I) == NA


def find_number_in_apron(K: dict, I: dict, It: dict) -> int:
    """
    :param K: Set of gates
    :param I: Set of aircraft
    :param It: Set of overlapping aircraft
    :return: Apron number
    """

    I_list = list(I.keys())
    end_node = max(I_list)+1
    nodes = [0] + list(I_list) + [end_node]
    K_len = len(K.keys()) - 1

    model = Model()
    Z = {}

    for i in nodes[1:]:  # Arcs from 0th node to all other nodes
        Z[0, i] = model.addVar(lb=0, ub=1, vtype=GRB.BINARY, name=f'x_{0}{i}')
    for i in nodes[1:-1]:  # Arcs to |I|th node from all other nodes
        Z[i, end_node] = model.addVar(lb=0, ub=1, vtype=GRB.BINARY, name=f'x_{i}{end_node}')

    for i in nodes[1:-1]:
        for j in nodes[1:-1]:
            # if aircraft i and j are in all present in any instance It_x of the overlapping set I_t and i is not j
            # create a link between the aircraft
            if not any(all(aircraft in It_x for aircraft in [i, j]) for It_x in list(It.values())) and i != j:
                Z[i, j] = model.addVar(lb=0, ub=1, vtype=GRB.BINARY, name=f'x_{i}{j}')
            else:
                Z[i, j] = 0

    model.update()
    C1 = model.addConstr((quicksum(Z[0, j] for j in nodes[1:]) <= K_len), name="C1")
    C2 = model.addConstr((quicksum(Z[i, end_node] for i in nodes[:-1]) <= K_len), name="C2")

    for i in nodes[1:-1]:
        C3 = model.addConstr((quicksum(Z[i, j] for j in nodes[1:-1]) == quicksum(Z[j, i] for j in nodes[1:-1])), name=f"C{3+i}")
    for i in nodes[1:-1]:
        C4 = model.addConstr((quicksum(Z[i, j] for j in nodes[1:]) <= 1), name=f"C{3+len(nodes[1:-1])+1}")

    obj = LinExpr()
    for i in nodes[:-1]:
        for j in nodes[1:]:
            obj += Z[i, j]

    model.setObjective(obj, GRB.MAXIMIZE)
    model.update()
    model.optimize()
    return len(I_list) + 1 - model.ObjVal
