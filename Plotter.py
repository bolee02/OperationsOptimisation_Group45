import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from main_dynamic import I, I_d, I_i, K, K_d, K_i, overlapping_aircraft_set, K_prime_d, K_prime_i,p, e, f, t
from model import model
import gurobipy as gp
from gurobipy import Model
from matplotlib.lines import Line2D

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
print('------')
print(ac_i)
print(ac_i_t)
print(g_i)

t_interval = [9,10,11,12,13,14,15]
# plotting
fig, ax = plt.subplots()
ax.set_yticks([10, 20, 30, 40, 50, 60 ,70, 80, 90])
ax.set_yticklabels(['Gate1', 'Gate2', 'Gate3', 'Gate4', 'Gate5', 'Gate6', 'Gate7', 'Gate8', 'Apron'])
apron_counter_10 = 1
apron_counter_12 = 1
apron_counter_14 = 1
apron_counter_15 = 1

for index,ac_num in enumerate(ac_d):
    start_time = t_interval[ac_d_t[index]]
    end_time = start_time + 2

    if(g_d[index]=='g1'):
        y_bottom_left = 7.5
        rect = Rectangle((start_time, y_bottom_left), 2, 5, edgecolor='b', facecolor='none')
        ax.add_patch(rect)
        ax.text(start_time+1, y_bottom_left+2.5, ac_num, ha='center', va='center', fontsize=10, color='black')

    elif (g_d[index] == 'g2'):
        y_bottom_left = 17.5
        rect = Rectangle((start_time, y_bottom_left), 2, 5, edgecolor='b', facecolor='none')
        ax.add_patch(rect)
        ax.text(start_time + 1, y_bottom_left + 2.5, ac_num, ha='center', va='center', fontsize=10, color='black')

    elif (g_d[index] == 'g3'):
        y_bottom_left = 27.5
        rect = Rectangle((start_time, y_bottom_left), 2, 5, edgecolor='b', facecolor='none')
        ax.add_patch(rect)
        ax.text(start_time + 1, y_bottom_left + 2.5, ac_num, ha='center', va='center', fontsize=10, color='black')

    elif (g_d[index] == 'g4'):
        y_bottom_left = 37.5
        rect = Rectangle((start_time, y_bottom_left), 2, 5, edgecolor='b', facecolor='none')
        ax.add_patch(rect)
        ax.text(start_time + 1, y_bottom_left + 2.5, ac_num, ha='center', va='center', fontsize=10, color='black')

    elif (g_d[index] == 'a'):
        y_bottom_left = 87.5
        rect = Rectangle((start_time, y_bottom_left), 2, 5, edgecolor='black', facecolor='none')
        ax.add_patch(rect)
        if (start_time == 10):
            if (apron_counter_10 > 0):
                ax.text(start_time + 1, y_bottom_left + 2.5 + 2.5 * 2 * apron_counter_10, str(ac_num), ha='center',
                        va='center', fontsize=10,
                        color='black')

            else:
                ax.text(start_time + 1, y_bottom_left + 2.5, str(ac_num), ha='center', va='center', fontsize=10,
                        color='black')
            apron_counter_10 += 1
        elif (start_time == 12):
            if (apron_counter_12 > 0):
                ax.text(start_time + 1, y_bottom_left + 2.5 + 2.5 * 2 * apron_counter_12, str(ac_num), ha='center',
                        va='center', fontsize=10,
                        color='black')

            else:
                ax.text(start_time + 1, y_bottom_left + 2.5, str(ac_num), ha='center', va='center', fontsize=10,
                        color='black')
            apron_counter_12 += 1
        elif (start_time == 14):
            if (apron_counter_14 > 0):
                ax.text(start_time + 1, y_bottom_left + 2.5 + 2.5 * 2 * apron_counter_14, str(ac_num), ha='center',
                        va='center', fontsize=10,
                        color='black')

            else:
                ax.text(start_time + 1, y_bottom_left + 2.5, str(ac_num), ha='center', va='center', fontsize=10,
                        color='black')
            apron_counter_14 += 1
        elif (start_time == 15):
            if (apron_counter_15 > 0):
                ax.text(start_time + 1, y_bottom_left + 2.5 + 2.5 * 2 * apron_counter_15, str(ac_num), ha='center',
                        va='center', fontsize=10,
                        color='black')

            else:
                ax.text(start_time + 1, y_bottom_left + 2.5, str(ac_num), ha='center', va='center', fontsize=10,
                        color='black')
            apron_counter_15 += 1
        else:
            ax.text(start_time + 1, y_bottom_left + 2.5 + 2.5 * 2, str(ac_num), ha='center', va='center', fontsize=10,
                    color='black')



for index,ac_num in enumerate(ac_i):
    start_time = t_interval[ac_i_t[index]]
    end_time = start_time + 2

    if(g_i[index]=='g5'):
        y_bottom_left = 47.5
        rect = Rectangle((start_time, y_bottom_left), 2, 5, edgecolor='r', facecolor='none')
        ax.add_patch(rect)
        ax.text(start_time+1, y_bottom_left+2.5, ac_num, ha='center', va='center', fontsize=10, color='black')

    elif (g_i[index] == 'g6'):
        y_bottom_left = 57.5
        rect = Rectangle((start_time, y_bottom_left), 2, 5, edgecolor='r', facecolor='none')
        ax.add_patch(rect)
        ax.text(start_time + 1, y_bottom_left + 2.5, ac_num, ha='center', va='center', fontsize=10, color='black')

    elif (g_i[index] == 'g7'):
        y_bottom_left = 67.5
        rect = Rectangle((start_time, y_bottom_left), 2, 5, edgecolor='r', facecolor='none')
        ax.add_patch(rect)
        ax.text(start_time + 1, y_bottom_left + 2.5, ac_num, ha='center', va='center', fontsize=10, color='black')

    elif (g_i[index] == 'g8'):
        y_bottom_left = 77.5
        rect = Rectangle((start_time, y_bottom_left), 2, 5, edgecolor='r', facecolor='none')
        ax.add_patch(rect)
        ax.text(start_time + 1, y_bottom_left + 2.5, ac_num, ha='center', va='center', fontsize=10, color='black')

    elif (g_i[index] == 'a'):
        y_bottom_left = 87.5
        rect = Rectangle((start_time, y_bottom_left), 2, 5, edgecolor='black', facecolor='none')
        ax.add_patch(rect)
        if (start_time==10):
            if (apron_counter_10>0):
                ax.text(start_time + 1, y_bottom_left + 2.5 + 2.5 * 2 * apron_counter_10, str(ac_num), ha='center', va='center', fontsize=10,
                        color='black')

            else:
                ax.text(start_time + 1, y_bottom_left + 2.5, str(ac_num), ha='center', va='center', fontsize=10,
                        color='black')
            apron_counter_10 += 1
        elif (start_time == 12):
            if (apron_counter_12>0):
                ax.text(start_time + 1, y_bottom_left + 2.5 + 2.5 * 2 * apron_counter_12, str(ac_num), ha='center', va='center', fontsize=10,
                        color='black')

            else:
                ax.text(start_time + 1, y_bottom_left + 2.5, str(ac_num), ha='center', va='center', fontsize=10,
                        color='black')
            apron_counter_12 += 1
        elif (start_time == 14):
            if (apron_counter_14>0):
                ax.text(start_time + 1, y_bottom_left + 2.5 + 2.5 * 2 * apron_counter_14, str(ac_num), ha='center', va='center', fontsize=10,
                        color='black')

            else:
                ax.text(start_time + 1, y_bottom_left + 2.5, str(ac_num), ha='center', va='center', fontsize=10,
                        color='black')
            apron_counter_14 += 1
        elif (start_time == 15):
            if (apron_counter_15>0):
                ax.text(start_time + 1, y_bottom_left + 2.5 + 2.5 * 2 * apron_counter_15, str(ac_num), ha='center', va='center', fontsize=10,
                        color='black')

            else:
                ax.text(start_time + 1, y_bottom_left + 2.5, str(ac_num), ha='center', va='center', fontsize=10,
                        color='black')
            apron_counter_15 += 1
        else:
            ax.text(start_time + 1, y_bottom_left + 2.5 + 2.5 * 2, str(ac_num), ha='center', va='center', fontsize=10, color='black')

plt.xlim([9, 17])
plt.ylim([0, 115])
plt.xlabel('Time [hrs]')
custom_lines = [Line2D([0], [0], color=cmap(), lw=4),
                Line2D([0], [0], color=cmap(.5), lw=4),
                Line2D([0], [0], color=cmap(1.), lw=4)]

plt.show()

