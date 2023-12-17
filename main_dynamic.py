from model import model
import random

total_pax = 20
min_num_aircraft = 5
max_num_aircraft = 20

def generate_random_interval_presence(keys, intervals):
    boolean_dict = {k: {t: 0 for t in intervals} for k in keys}
    for k in boolean_dict:
        start_time = random.randint(1, len(intervals.keys()))
        boolean_dict[k][start_time] = 1
        boolean_dict[k][start_time+1] = 1
    return boolean_dict
def generate_random_integer_dict(keys, max_value):
    return {k: random.randint(0, max_value) for k in keys}

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
    "a": {"g1": 151, "g2": 151, "g3": 151, "g4": 151, "e": 151}  # Apron
}

# Set of international gates
K_i = {
    "g5": {"g5": 0, "g6": 50, "g7": 100, "g8": 150, "e": 50},
    "g6": {"g5": 50, "g6": 0, "g7": 50, "g8": 100, "e": 50},
    "g7": {"g5": 100, "g6": 50, "g7": 0, "g8": 50, "e": 50},
    "g8": {"g5": 150, "g6": 100, "g7": 50, "g8": 0, "e": 50},
    "a": {"g1": 151, "g2": 151, "g3": 151, "g4": 151, "e": 151}  # Apron
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
num_aircraft = random.randint(min_num_aircraft, max_num_aircraft)
aircraft = list(range(1, num_aircraft + 1))
I = {i: random.choice([0, 1]) for i in aircraft}

# Set of all domestic aircraft and presence in time intervals
I_d = generate_random_interval_presence({k: v for k, v in I.items() if v == 1}.keys(), t)

# Set of all international aircraft and presence in time intervals
I_i = generate_random_interval_presence({k: v for k, v in I.items() if v == 0}.keys(), t)

# Number of passengers arriving from each aircraft
pax_arr = generate_random_integer_dict(aircraft, total_pax)

# Number of passengers leaving the airport via its exit from aircraft i
f = {k: v-random.randint(0, v) for k, v in pax_arr.items()}

# Number of passengers transiting from aircraft i
pax_tra = {k: pax_arr[k] - v1 for k, v1 in f.items()}

def possible_transfer_aircraft(aircraft_num, I):
    if I[aircraft_num] == 1:
        I_k = I_d
    else:
        I_k = I_i
    for k, v in I_k[aircraft_num].items():
        if v == 1:
            return k

# Number of passengers transiting from aircraft i to aircraft j
def generate_transiting_passengers(aircraft, pax_tra):
    p = {k: {k: 0 for k in aircraft} for k in aircraft}
    for k in pax_tra:
        pax_tra_hold = pax_tra[k]
        for i in range(possible_transfer_aircraft(k, I), len(aircraft)+1):
            pax = random.randint(0, pax_tra_hold)
            p[k][i] = pax
            if i == k:
                p[k][i] = 0
            else:
                pax_tra_hold -= pax
    return p


p = generate_transiting_passengers(aircraft, pax_tra)

# Number of passengers coming from entrance of the airport to aircraft i
def generate_entering_passengers(p, aircraft):
    pax_transin = {k: 0 for k in aircraft}
    for k in p:
        for j in p[k]:
            pax_transin[j] += p[k][j]
    e = {k: random.randint(0, (total_pax-v)) for k, v in pax_transin.items()}
    return e


e = generate_entering_passengers(p, aircraft)

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