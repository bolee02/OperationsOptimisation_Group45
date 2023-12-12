from gurobipy import Model, GRB, LinExpr
from constraints.constr3 import plane_assigned_to_only_one_gate
from constraints.constr4_5 import one_aircraft_at_gate
from constraints.constr6 import number_of_aircraft_in_the_apron
from constraints.constr10_11 import transit_leaving, transit_coming
import random

def generate_random_boolean_dict(keys, intervals):
    return {k: {t: random.choice([0, 1]) for t in intervals} for k in keys}
def generate_random_integer_dict(keys, max_value):
    return {k: random.randint(0, max_value) for k in keys}

# Set of all gates, 1 if domestic, 0 if international
num_gates = random.randint(1, 10)
gates = [f"g{i}" for i in range(1, num_gates + 1)]
K = {gate: random.choice([0, 1]) for gate in gates}
K.update({"a": 0})

# Set of domestic gates
K.update({"e": 1})
domestic_gates = [gate for gate, is_domestic in K.items() if is_domestic]
K_d = {gate: generate_random_integer_dict(domestic_gates, 100) for gate in domestic_gates}

# Set of international gates
K.update({"e": 0})
international_gates = [gate for gate, is_domestic in K.items() if not is_domestic]
K_i = {gate: generate_random_integer_dict(international_gates, 100) for gate in international_gates}

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
num_aircraft = random.randint(1, 14)
aircraft = list(range(1, num_aircraft + 1))
I = {i: random.choice([0, 1]) for i in aircraft}

# Set of all domestic aircraft and presence in time intervals
I_d = generate_random_boolean_dict(aircraft[:num_gates], t)

# Set of all international aircraft and presence in time intervals
I_i = generate_random_boolean_dict(aircraft[num_gates:], t)

# Number of passengers coming from entrance of the airport to aircraft i
e = generate_random_integer_dict(aircraft, 0)

# Number of passengers leaving the airport via its exit after the arrival of aircraft i
f = generate_random_integer_dict(aircraft, 0)

# Number of passengers transiting from aircraft i to aircraft j
p = {i: generate_random_integer_dict(aircraft, 0) for i in aircraft}

# Set of aircraft overlapping at time interval t - I_Dt or I_It
def overlapping_aircraft(I: dict, t_i):
    I_t = {}
    for k, v in I.items():
        if v.get(t_i, 0) == 1:
            I_t.setdefault(k, []).append(t_i)
    if len(I_t.keys()) > 1:
        return I_t


# Set containing I_Dt or I_It for all t - T_D or T_I
def overlapping_aircraft_set(I: dict, t: dict):
    T = {}
    for k in t:
        result = overlapping_aircraft(I, k)
        if result:
            T[k] = list(result.keys())
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
T_D = overlapping_aircraft_set(I_d, t)
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