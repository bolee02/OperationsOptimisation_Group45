import numpy as np
from gurobipy import quicksum


def one_aircraft_at_gate_old(x, T, K_prime) -> np.ndarray:
    """
    Conditions to check each gate in time interval T has 1 or less planes assigned
    :param x: numpy array: 1 if aircraft 𝑖 is assigned to gate 𝑘, and 0 otherwise.
    :type x: np.ndarray
    :param T: set of all aircraft overlapping in time interval t
    :type T: np.ndarray
    :param K_prime: set of fixed gates
    :type K_prime: np.ndarray
    :return: np.ndarray
    """
    array_time_gates = np.array((len(T), len(K_prime)), dtype=bool)

    for dt_index, Dt_set in enumerate(T):
        for k in range(len(K_prime)):
            array_time_gates[dt_index, k] = np.sum(x[Dt_set, k]) <= 1

    return array_time_gates


def one_aircraft_at_gate(x, I_t: dict, k):
    """
    Conditions to check each gate in time interval T has 1 or less planes assigned
    :param x: numpy array: 1 if aircraft 𝑖 is assigned to gate 𝑘, and 0 otherwise.
    :type x: dict
    :param I_t: set of all aircraft (either domestic or international) overlapping in time interval t
    :type I_t: dict
    """
    return quicksum(x[i, k] for i in I_t) <= 1


def one_aircraft_at_gateV2(x: dict, z: dict, I_t: dict, k: dict):
    """
    Conditions to check each gate in time interval T has 1 or less planes assigned
    :param x: 1 if aircraft 𝑖 is assigned to arrive at gate 𝑘, and 0 otherwise.
    :param z: 1 if aircraft 𝑖 is assigned to depart from gate 𝑘, and 0 otherwise.
    :param I_t: set of all aircraft (either domestic or international) overlapping in time interval t
    """
    return quicksum(x[i, k] + z[i, k] for i in I_t) <= 1
