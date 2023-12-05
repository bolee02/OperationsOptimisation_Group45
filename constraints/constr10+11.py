import numpy as np

def transit_leaving(x,y_ijkl,e_i,p_ij) -> np.ndarray:
    """
    Condition to ensure all transit passengers of aircraft i travel from assigned gate k to other gates
    :param x: numpy array: 1 if aircraft 𝑖 is assigned to gate 𝑘, and 0 otherwise. (decision variable)
    :type x: np.ndarray
    :param y_ijkl: fraction of passengers transiting from a/c i to j via gates k and l
    (of each i, a fraction for each gate) (rows: ac/s, columns: gates
    :type y_ijkl: np.ndarray
    :param e_i: # of passengers in a/c i
    :type e_i: np.ndarray (1D)
    :param p_ij: # of passengers transiting from a/c i to a/c to j
    :type p_ij: np.ndarray
    :return: an array that returns true for each a/c i if condition is made, false otherwise
    """
    #two arrays for boolean checking
    RHS_arr = []
    LHS_arr = []
    for ac_index,ac2gate in enumerate(x):
        #total passengers coming out from a/c i
        passengers = e_i[ac_index]
        #find the assigned gate
        k = np.nonzero(ac2gate)[0]
        #if there is an assigned gate k
        if len(k) > 0:
            #total passengers transiting from a/c i (RIGHT HAND SIDE)
            RHS = np.sum(p_ij[ac_index])
            RHS_arr.append(RHS)
            #passengers of a/c i travelling from gate k to other gates
            LHS = passengers*np.sum(y_ijkl[ac_index]) #sigma(wikl)
            LHS_arr.append(LHS)

    condition = np.equal(RHS_arr,LHS_arr)
    return condition

def transit_coming(x,y_ijkl,e_i,p_ij) -> np.ndarray:
    """
    Condition to ensure all transit passengers of i travelling to k from all other gates
    :param x: numpy array: 1 if aircraft 𝑖 is assigned to gate 𝑘, and 0 otherwise. (decision variable)
    :type x: np.ndarray
    :param y_ijkl: fraction of passengers transiting from a/c i to j via gates k and l
    (of each i, a fraction for each gate) (rows: ac/s, columns: gates
    :type y_ijkl: np.ndarray
    :param e_i: # of passengers in a/c i
    :type e_i: np.ndarray (1D)
    :param p_ij: # of passengers transiting from a/c i to a/c to j
    :type p_ij: np.ndarray
    :return: an array that returns true for each a/c i if condition is made, false otherwise
    """
    #two arrays for boolean checking
    RHS_arr = []
    LHS_arr = []
    for ac_index,ac2gate in enumerate(x):
        #total passengers coming out from a/c i
        passengers = e_i[ac_index]
        #find the assigned gate of i
        k_i = np.nonzero(ac2gate)[0]
        #for j = 0











