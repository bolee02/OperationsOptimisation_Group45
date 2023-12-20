import gurobipy as gp
from gurobipy import GRB
import subprocess
from main_dynamic import I, I_d, I_i, K, K_d, K_i, overlapping_aircraft_set, K_prime_d, K_prime_i,p, e, f, t
from model import model



# subprocess.run(["python", "main_dynamic.py"])
# m_base = gp.read('MPS.mps')
# m_base.optimize()
# objValue_base = m_base.ObjVal
#
#arrival delayed 1 hour
# I_d[1] = {1: 0, 2: 0, 3: 1, 4: 1, 5: 0, 6: 0, 7: 0, 8: 0}
# M = model(I, I_d, I_i,
#       K, K_d, K_i,
#       overlapping_aircraft_set(I_d, t), overlapping_aircraft_set(I_i, t),
#       K_prime_d, K_prime_i,
#       p, e, f)
# m_delayed = gp.read('MPS.mps')
# m_delayed.optimize()
# objValue_delayed = m_delayed.ObjVal

#arrival delayed 2 hours
I_d[1] = {1: 0, 2: 0, 3: 0, 4: 1, 5: 1, 6: 0, 7: 0, 8: 0}
M = model(I, I_d, I_i,
      K, K_d, K_i,
      overlapping_aircraft_set(I_d, t), overlapping_aircraft_set(I_i, t),
      K_prime_d, K_prime_i,
      p, e, f)
m_delayed = gp.read('MPS.mps')
m_delayed.optimize()
objValue_delayed = m_delayed.ObjVal
objValue_arr = []




for v in range (6):
      if v ==0:
            subprocess.run(["python", "main_dynamic.py"])
            m_base = gp.read('MPS.mps')
            m_base.optimize()
            objValue_base = m_base.ObjVal
            print('THIS', objValue_delayed)
            print(v)
            objValue_arr.append(objValue_base)
      elif v==1:
            I_d[1] = {1: 0, 2: 0, 3: 1, 4: 1, 5: 0, 6: 0, 7: 0, 8: 0}
            M = model(I, I_d, I_i,K, K_d, K_i,overlapping_aircraft_set(I_d, t), overlapping_aircraft_set(I_i, t),K_prime_d, K_prime_i,p, e, f)
            m_delayed = gp.read('MPS.mps')
            m_delayed.optimize()
            objValue_delayed = m_delayed.ObjVal
            print('THIS', objValue_delayed)
            print(v)
            objValue_arr.append(objValue_delayed)
      elif v==2:
            I_d[1] = {1: 0, 2: 0, 3: 0, 4: 1, 5: 1, 6: 0, 7: 0, 8: 0}
            M = model(I, I_d, I_i,K, K_d, K_i,overlapping_aircraft_set(I_d, t), overlapping_aircraft_set(I_i, t),K_prime_d, K_prime_i,p, e, f)
            m_delayed = gp.read('MPS.mps')
            m_delayed.optimize()
            objValue_delayed = m_delayed.ObjVal
            print('THIS', objValue_delayed)
            print(v)
            objValue_arr.append(objValue_delayed)
      elif v == 3:
            I_d[1] = {1: 0, 2: 0, 3: 0, 4: 0, 5: 1, 6: 1, 7: 0, 8: 0}
            M = model(I, I_d, I_i, K, K_d, K_i, overlapping_aircraft_set(I_d, t), overlapping_aircraft_set(I_i, t),
                      K_prime_d, K_prime_i, p, e, f)
            m_delayed = gp.read('MPS.mps')
            m_delayed.optimize()
            objValue_delayed = m_delayed.ObjVal
            print('THIS', objValue_delayed)
            print(v)
            objValue_arr.append(objValue_delayed)
      elif v == 4:
            I_d[1] = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 1, 7: 1, 8: 0}
            M = model(I, I_d, I_i, K, K_d, K_i, overlapping_aircraft_set(I_d, t), overlapping_aircraft_set(I_i, t),
                      K_prime_d, K_prime_i, p, e, f)
            m_delayed = gp.read('MPS.mps')
            m_delayed.optimize()
            objValue_delayed = m_delayed.ObjVal
            print('THIS', objValue_delayed)
            print(v)
            objValue_arr.append(objValue_delayed)
      elif v == 5:
            I_d[1] = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 1, 8: 1}
            M = model(I, I_d, I_i, K, K_d, K_i, overlapping_aircraft_set(I_d, t), overlapping_aircraft_set(I_i, t),
                      K_prime_d, K_prime_i, p, e, f)
            m_delayed = gp.read('MPS.mps')
            m_delayed.optimize()
            objValue_delayed = m_delayed.ObjVal
            print('THIS',objValue_delayed)
            print(v)
            objValue_arr.append(objValue_delayed)

print(objValue_arr)





