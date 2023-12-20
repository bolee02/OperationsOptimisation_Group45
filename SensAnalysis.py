import gurobipy as gp
from gurobipy import GRB
import subprocess
from main_dynamic import I, I_d, I_i, K, K_d, K_i, overlapping_aircraft_set, K_prime_d, K_prime_i,p, e, f, t
from model import model


I_d[1] = {1: 1, 2: 1, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0}

###FLIGHT DELAY####
model(I, I_d, I_i,
      K, K_d, K_i,
      overlapping_aircraft_set(I_d, t), overlapping_aircraft_set(I_i, t),
      K_prime_d, K_prime_i,
      p, e, f)

def make_first_one_zero(input_dict):
    for key, value in input_dict.items():
        if value != 0:
            input_dict[key] = 0
            break
    return input_dict

def make_next_after_first_nonzero_one(input_dict):
    found_nonzero = False
    for key, value in input_dict.items():
        if found_nonzero:
            input_dict[key] = 1
            break
        if value != 0:
            found_nonzero = True
    return input_dict

objValue_arr = []
delay_arr = []
m_base = gp.read('MPS.mps')
m_base.optimize()
objValue_base = m_base.ObjVal
objValue_arr.append(objValue_base)
delay_arr.append(0)

for delay in range (6):
    delay_arr.append(delay+1)
    I_d[1] = make_first_one_zero(I_d[1])
    I_d[1] = make_next_after_first_nonzero_one(I_d[1])
    model(I, I_d, I_i, K, K_d, K_i, overlapping_aircraft_set(I_d, t), overlapping_aircraft_set(I_i, t), K_prime_d,
          K_prime_i, p, e, f)
    m_delayed = gp.read('MPS.mps')
    m_delayed.optimize()
    objValue_delayed = m_delayed.ObjVal
    objValue_arr.append(objValue_delayed)

print(delay_arr)
print(objValue_arr)
####FLIGHT CANCELLATION####








