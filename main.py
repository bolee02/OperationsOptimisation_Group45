from gurobipy import Model, GRB, LinExpr
from constraints.constr3 import plane_assigned_to_only_one_gate
from constraints.constr4_5 import one_aircraft_at_gate
from constraints.constr6 import number_of_aircraft_in_the_apron
from constraints.constr10_11 import transit_leaving, transit_coming

# Set of all gates, 1 if domestic, 0 if international
K = {
    "g1": 1,
    "g2": 1,
    "g3": 1,
    "g4": 1,
    "g5": 0,
    "g6": 0,
    "g7": 0,
    "g8": 0,
    "a": 0
}

# Set of domestic gates
K_d = {
    "g1": {"g1": 0, "g2": 50, "g3": 100, "g4": 150, "e": 50},
    "g2": {"g1": 50, "g2": 0, "g3": 50, "g4": 100, "e": 50},
    "g3": {"g1": 100, "g2": 50, "g3": 0, "g4": 50, "e": 50},
    "g4": {"g1": 150, "g2": 100, "g3": 50, "g4": 0, "e": 50},
    "a": {"g1": GRB.INFINITY, "g2": GRB.INFINITY, "g3": GRB.INFINITY, "g4": GRB.INFINITY, "e": GRB.INFINITY}  # Apron
}

# Set of international gates
K_i = {
    "g5": {"g5": 0, "g6": 50, "g7": 100, "g8": 150, "e": 50},
    "g6": {"g5": 50, "g6": 0, "g7": 50, "g8": 100, "e": 50},
    "g7": {"g5": 100, "g6": 50, "g7": 0, "g8": 50, "e": 50},
    "g8": {"g5": 150, "g6": 100, "g7": 50, "g8": 0, "e": 50},
    "a": {"g1": GRB.INFINITY, "g2": GRB.INFINITY, "g3": GRB.INFINITY, "g4": GRB.INFINITY, "e": GRB.INFINITY}  # Apron
}

# Set of all fixed domestic gates
K_prime_d = set(K_d.keys()) - {"a"}

# Set of all fixed international gates
K_prime_i = set(K_i.keys()) - {"a"}

# Set of time intervals
t = {
    1: "09:00-10:00",
    2: "10:00-11:00",
    3: "11:00-12:00",
    4: "12:00-13:00",
    5: "13:00-14:00",
    6: "14:00-15:00",
    7: "15:00-16:00",
    8: "16:00-17:00"
}

# Set of all aircraft, 1 if domestic, 0 if international
I = {
    1: 1,
    2: 1,
    3: 1,
    4: 1,
    5: 1,
    6: 1,
    7: 1,
    8: 0,
    9: 0,
    10: 0,
    11: 0,
    12: 0,
    13: 0,
    14: 0
}

# Set of all domestic aircraft and presence in time intervals
I_d = {
    1: {1: 1, 2: 1, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0},
    2: {1: 0, 2: 1, 3: 1, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0},
    3: {1: 0, 2: 0, 3: 1, 4: 1, 5: 0, 6: 0, 7: 0, 8: 0},
    4: {1: 0, 2: 0, 3: 0, 4: 1, 5: 1, 6: 0, 7: 0, 8: 0},
    5: {1: 0, 2: 0, 3: 0, 4: 0, 5: 1, 6: 1, 7: 0, 8: 0},
    6: {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 1, 7: 1, 8: 0},
    7: {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 1, 8: 1}
}

# Set of all international aircraft and presence in time intervals
I_i = {
    8: {1: 1, 2: 1, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0},
    9: {1: 0, 2: 1, 3: 1, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0},
    10: {1: 0, 2: 0, 3: 1, 4: 1, 5: 0, 6: 0, 7: 0, 8: 0},
    11: {1: 0, 2: 0, 3: 0, 4: 1, 5: 1, 6: 0, 7: 0, 8: 0},
    12: {1: 0, 2: 0, 3: 0, 4: 0, 5: 1, 6: 1, 7: 0, 8: 0},
    13: {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 1, 7: 1, 8: 0},
    14: {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 1, 8: 1}
}

# Number of passengers coming from entrance of airport to aircraft i
e = {
    1: 0,
    2: 0,
    3: 0,
    4: 0,
    5: 0,
    6: 0,
    7: 0,
    8: 0,
    9: 0,
    10: 0,
    11: 0,
    12: 0,
    13: 0,
    14: 0
}

# Number of passengers leaving the airport via its exit after the arrival of aircraft i
f = {
    1: 0,
    2: 0,
    3: 0,
    4: 0,
    5: 0,
    6: 0,
    7: 0,
    8: 0,
    9: 0,
    10: 0,
    11: 0,
    12: 0,
    13: 0,
    14: 0
}

# Number of passengers transiting from aircraft i to aircraft j
p = {
    1: {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0},
    2: {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0},
    3: {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0},
    4: {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0},
    5: {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0},
    6: {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0},
    7: {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0},
    8: {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0},
    9: {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0},
    10: {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0},
    11: {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0},
    12: {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0},
    13: {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0},
    14: {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0}
}

# Set of aircraft overlapping at time interval t - I_Dt or I_It
def overlapping_aircraft(I: dict, t_i: dict):
    I_t = {k: v for k, v in I.items() if v[t_i] == 1}
    if len(I_t) == 1:
        return dict()
    return I_t


# Set containing I_Dt or I_It for all t - T_D or T_I
def overlapping_aircraft_set(I: dict, t: dict):
    T = {k: overlapping_aircraft(I, k) for k in t}
    return T


"""
                    Start of Model definition
"""
constraint_counter = 1

model = Model()
x = dict()
"Create x. lb is lower bound; ub is upper bound; vtype is variable type"
for i in list(I.keys()):
    for j in list(K.keys()):
        x[i, j] = model.addVar(lb=0, ub=1, vtype=GRB.BINARY, name=f'x_{i}{j}')

model.update()
""" Refrenced in paper as equation (3). Forces plane to be ony assigned to one gate. Boolean condition is to check if 
    the flight is domestic, then domestic gates can be used, or international, then only domestic gates can be used """
for i in list(I.keys()):
    K_gi = K_d if bool(I[i]) else K_i
    model.addConstr(plane_assigned_to_only_one_gate(x, i, K_d), name=f"C{constraint_counter}")
    constraint_counter += 1

""" Refrenced in paper as equation (4). Checks that for a certain time period, only one aircraft is assigned to a 
    domestic gate """
T_D = list(overlapping_aircraft_set(I_d, t))
for I_dt in T_D:
    for k in K_prime_d:
        model.addConstr(one_aircraft_at_gate(x, I_dt), name=f"C{constraint_counter}")
        constraint_counter += 1

""" Refrenced in paper as equation (5). Checks that for a certain time period, only one aircraft is assigned to a 
    international gate """
T_I = list(overlapping_aircraft_set(I_i, t))
for I_it in T_I:
    for k in K_prime_i:
        model.addConstr(one_aircraft_at_gate(x, I_it), name=f"C{constraint_counter}")
        constraint_counter += 1


""" Refrenced in paper as equation (6). Checks that the number of aircraft in the apron is the same as the assigned 
    number """
model.addConstr(number_of_aircraft_in_the_apron(x, K_d, I_d, T_D, K_i, I_i, T_I), name=f"C{constraint_counter}")
constraint_counter += 1


""" Refrenced in paper as equation (10). """
w = {1: {1: {1: "a"}}}

for i in list(I.keys()):
    K_gi = K_d if bool(I[i]) else K_i
    for k in list(K_gi):
        """ I think gurobi will optimise away all the non relevant values of k but look at the comment in constr10_11"""
        model.addConstr(transit_leaving(x, K, I, p, w, i, k), name=f"C{constraint_counter}")
        constraint_counter += 1

for i in list(I.keys()):
    K_gi = K_d if I[i] else K_i
    for k in list(K):
        """ I think gurobi will optimise away all the non relevant values of k but look at the comment in constr10_11"""
        model.addConstr(transit_leaving(x, K_gi, I, p, w, i, k), name=f"C{constraint_counter}")
        constraint_counter += 1

obj = LinExpr()
for i in list(I.keys()):
    K_gi = K_d if I[i] else K_i
    for k in list(K_gi.keys()):
        for l in list(K_gi.keys()):
            obj += w[i, k, l] * K_gi[k, l]

        obj += (e[i] + f[i]) * K_gi[k, "e"] * x[i, k]

model.setObjective(obj, GRB.MINIMIZE)
model.update()
model.optimize()