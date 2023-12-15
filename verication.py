from model import model
from gurobipy import GRB

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


I = {1: 1,
     2: 0,
     3: 0,
     4: 1}

I_d = {1: {1: 1, 2: 1, 3: 0},
       4: {1: 0, 2: 1, 3: 1}}
I_i = {2: {1: 1, 2: 1, 3: 0},
       3: {1: 1, 2: 1, 3: 0}}

K = {"g1": 1, "g2": 0, "a": 0}
K_d = {"g1": {"g1": 0, "g2": 10, "e": 20, "a": 40},
       "a": {"g1": 40, "g2": 40, "e": 40, "a": 40}}
K_i = {"g2": {"g1": 10, "g2": 0, "e": 20, "a": 40},
       "a": {"g1": 40, "g2": 40, "e": 40, "a": 40}}

t = {1: 1, 2: 2, 3: 3}

T_D = overlapping_aircraft_set(I_d, t)
T_I = overlapping_aircraft_set(I_i, t)

K_prime_d = set(K_d.keys()) - {"a"}
K_prime_i = set(K_i.keys()) - {"a"}

p = {1: {1: 0, 2: 50, 3: 50, 4: 50},  # 200 in the plane
     2: {1: 50, 2: 0, 3: 50, 4: 50},  # 200 in the plane
     3: {1: 50, 2: 50, 3: 0, 4: 50},  # 200 in the plane
     4: {1: 50, 2: 50, 3: 50, 4: 0}}  # 200 in the plane

e = {1: 100, 2: 100, 3: 100, 4: 100}
f = {1: 50, 2: 50, 3: 50, 4: 50}

# from constraints.constr6 import find_number_in_apron
# print(find_number_in_apron(
#     {
#         "g1": {"g1": 0, "g2": 10, "e": 20, "a": 0},
#         "g2": {"g1": 10, "g2": 00, "e": 20, "a": 0},
#         "a": {"g1": 0, "g2": 0, "e": 0, "a": 0}
#     },
#     {
#         1: {1: 1, 2: 0, 3: 0},
#         2: {1: 1, 2: 1, 3: 0},
#         3: {1: 0, 2: 1, 3: 1},
#         4: {1: 0, 2: 1, 3: 1},
#         6: {1: 0, 2: 0, 3: 1},
#     },
#     {
#         1: [1, 2],
#         2: [2, 3, 4],
#         3: [3, 4, 5]
#     }
# ))
# print(find_number_in_apron(
#     {
#         "g1": {"g1": 0, "g2": 10, "e": 20, "a": 0},
#         "g2": {"g1": 10, "g2": 00, "e": 20, "a": 0},
#         "a": {"g1": 0, "g2": 0, "e": 0, "a": 0}
#     },
#     {
#         1: {1: 1, 2: 0, 3: 0},
#         2: {1: 1, 2: 0, 3: 0},
#         3: {1: 0, 2: 1, 3: 0},
#         4: {1: 0, 2: 1, 3: 0},
#         6: {1: 0, 2: 0, 3: 1},
#     },
#     {
#         1: [1, 2],
#         2: [3, 4],
#         3: []
#     }
# ))

model(I, I_d, I_i, K, K_d, K_i, T_D, T_I, K_prime_d, K_prime_i, p, e, f)