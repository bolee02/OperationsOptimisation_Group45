import numpy as np

def gate_assigned_to_only_one_gate(x, K, I):
    array = np.array((len(I), 1))
    for i in range(len(I)):
        array[i] = sum(x[i]) == 1


