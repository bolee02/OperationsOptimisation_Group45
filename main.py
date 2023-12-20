from gurobipy import GRB
from model import model

# Set of all gates, 1 if domestic, 0 if international
K = {
    "g1": 1,
    "g2": 1,
    "a": 0
}

# Set of domestic gates
K_d = {
    "g1": {"g1": 0, "g2": 50, "g3": 100, "e": 50,  "a": 500},
    "g2": {"g1": 50, "g2": 0, "g3": 50, "e": 50,  "a": 500},
    "a": {"g1": 500, "g2": 500, "g3": 500, "e": 500,  "a": 0}  # Apron
}

# Set of international gates
K_i = {
    "a": {"g1": 500, "g2": 500, "g3": 500, "e": 500, "a": 0}  # Apron
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
}

# Set of all domestic aircraft and presence in time intervals
I_d = {
    1: {1: 1, 2: 1, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0},
    2: {1: 1, 2: 1, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0},
    3: {1: 1, 2: 1, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0},
}

# Set of all international aircraft and presence in time intervals
I_i = {}

# Number of passengers coming from entrance of airport to aircraft i
e = {
    1: 8,
    2: 8,
    3: 8,
}

# Number of passengers leaving the airport via its exit after the arrival of aircraft i
f = {
    1: 4,
    2: 4,
    3: 4,
}

# Number of passengers transiting from aircraft i to aircraft j
p = {
    1: {1: 0, 2: 2, 3: 2},
    2: {1: 2, 2: 0, 3: 2},
    3: {1: 2, 2: 2, 3: 0},

}

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


model(I, I_d, I_i,
      K, K_d, K_i,
      overlapping_aircraft_set(I_d, t), overlapping_aircraft_set(I_i, t),
      K_prime_d, K_prime_i,
      p, e, f)