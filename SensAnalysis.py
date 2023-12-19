import gurobipy as gp
from gurobipy import GRB
import subprocess
from main_dynamic import generate_random_interval_presence, I, I_d, I_i, K, K_d, K_i, overlapping_aircraft_set, K_prime_d, K_prime_i,p, e, f, t
from model import model



scenario_max = 1

# for scenario in range (scenario_max):
subprocess.run(["python", "main_dynamic.py"])
m_base = gp.read('MPS.mps')
m_base.optimize()
#     optObjVal = m_base.ObjVal
#     dec_vars_opt = m_base.getVars()
#     NA_opt = m_base.
#     newObjVal = optObjVal
#     while(newObjVal == optObjVal):
#         NA_new =
# Var/Constr attributes to print

var_attrs = ('VarName', 'X', 'SAObjLow', 'SAObjUp')
con_attrs = ('ConstrName', 'Pi', 'SARHSLow', 'SARHSUp')

# Print formatted tables
head_fmt = '\n{:12s}' + '{:>15s}' * 3
row_fmt = '{:12s}' + '{:>15.6f}' * 3
print(head_fmt.format(*var_attrs))
for v in m_base.getVars():
    print(row_fmt.format(*map(lambda x: v.getAttr(x), var_attrs)))
print(head_fmt.format(*con_attrs))
for c in m_base.getConstrs():
    print(row_fmt.format(*map(lambda x: c.getAttr(x), con_attrs)))



