import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from main_dynamic import I, I_d, I_i, K, K_d, K_i, overlapping_aircraft_set, K_prime_d, K_prime_i,p, e, f, t
from model import model
import gurobipy as gp
from gurobipy import Model

I_d[1] = {1: 1, 2: 1, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0}
model(I, I_d, I_i,
      K, K_d, K_i,
      overlapping_aircraft_set(I_d, t), overlapping_aircraft_set(I_i, t),
      K_prime_d, K_prime_i,
      p, e, f)
m_base = gp.read('MPS.mps')
m_base.optimize()


ac_d = []   #domestic a/c number
ac_i = []   #international a/c number

ac_d_t = [] #domestic a/c start time index
ac_i_t = [] #international a/c start time index

g_d = [] #domestic a/c gates
g_i = []


for key, sub_dict in I_d.items():
    for index, value in enumerate(sub_dict.values()):
        if value != 0:
            ac_d.append(key)
            ac_d_t.append(index)
            break

for key, sub_dict in I_i.items():
    for index, value in enumerate(sub_dict.values()):
        if value != 0:
            ac_i.append(key)
            ac_i_t.append(index)
            break

for domestic_ac in ac_d:
    for k in K_d.keys():
        if m_base.getVarByName(f"x_{domestic_ac}{k}").X >= 0.99:
            g_d.append(k)

for int_ac in ac_i:
    for k in K_i.keys():
        if m_base.getVarByName(f"x_{int_ac}{k}").X >= 0.99:
            g_i.append(k)

print(ac_d)
print(ac_d_t)
print(g_d)

t_interval = [9,10,11,12,13,14,15]
# plotting
fig, ax = plt.subplots()
ax.set_yticks([10, 20, 30, 40, 50, 60 ,70, 80, 90])
ax.set_yticklabels(['Gate1', 'Gate2', 'Gate3', 'Gate4', 'Gate5', 'Gate6', 'Gate7', 'Gate8', 'Apron'])

for index,ac_num in enumerate(ac_d):
    start_time = t_interval[ac_d_t[index]]
    end_time = start_time + 2
    if(g_d[index]=='g1'):
        y_bottom_left = 5
        rect = Rectangle((start_time, y_bottom_left), 2, 10, edgecolor='b', facecolor='none')
        ax.add_patch(rect)
        ax.text(start_time+1, y_bottom_left+5, ac_num, ha='center', va='center', fontsize=12, color='b')

plt.xlim([9, 17])
plt.ylim([0, 110])
plt.show()

