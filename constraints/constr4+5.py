import numpy as np


def one_aircraft_at_gate(x, T, K_prime) -> np.ndarray:
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

