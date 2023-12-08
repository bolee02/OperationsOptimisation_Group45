from gurobipy import GRB
from constraints.constr6 import find_number_in_apron


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
    "g1": {"g1": 0, "g2": 50, "g3": 100, "g4": 150, "e": 50},
    "g2": {"g1": 50, "g2": 0, "g3": 50, "g4": 100, "e": 50},
    "g3": {"g1": 100, "g2": 50, "g3": 0, "g4": 50, "e": 50},
    "g4": {"g1": 150, "g2": 100, "g3": 50, "g4": 0, "e": 50},
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
    1: {1: 1, 2: 1, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0},
    2: {1: 0, 2: 1, 3: 1, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0},
    3: {1: 0, 2: 0, 3: 1, 4: 1, 5: 0, 6: 0, 7: 0, 8: 0},
    4: {1: 0, 2: 0, 3: 0, 4: 1, 5: 1, 6: 0, 7: 0, 8: 0},
    5: {1: 0, 2: 0, 3: 0, 4: 0, 5: 1, 6: 1, 7: 0, 8: 0},
    6: {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 1, 7: 1, 8: 0},
    7: {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 1, 8: 1}
}

# Set of all aircraft
I = {
    "d": I_d,
    "i": I_i
}


# Set of aircraft overlapping at time interval t - I_Dt or I_It
def overlapping_aircraft(I, t_i):
    I_t = {k: v for k, v in I.items() if v[t_i] == 1}
    if len(I_t) == 1:
        return dict()
    return I_t


# Set containing I_Dt or I_It for all t - T_D or T_I
def overlapping_aircraft_set(I, t):
    T = {k: overlapping_aircraft(I, k) for k in t}
    return T


print("Done")