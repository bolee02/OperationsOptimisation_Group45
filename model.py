from gurobipy import Model, GRB, LinExpr
from constraints.constr3 import plane_assigned_to_only_one_gate
from constraints.constr4_5 import one_aircraft_at_gate
from constraints.constr6 import number_of_aircraft_in_the_apron, find_number_in_apron
from constraints.constr10_11 import transit_leaving, transit_coming


def model(I: dict, I_d: dict, I_i: dict, K: dict, K_d: dict, K_i: dict, T_D: dict, T_I: dict, K_prime_d: dict,
          K_prime_i: dict, p: dict, e: dict, f: dict):
    """
    :param I: All aircraft
    :param I_d: All domestic aircraft
    :param I_i: All international aircraft
    :param K: All gates
    :param K_d: All domestic gates
    :param K_i: All internation gates
    :param T_D: All sets of overlapping domestic aircraft for all time instances t
    :param T_I: All sets of overlapping international aircraft for all time instances t
    :param K_prime_d:
    :param K_prime_i:
    :param p: Passenger numbers from aircraft to aircraft
    :param e: Passenger numbers from entrance to aircraft
    :param f: Passenger numbers from aircraft to exit
    :param w: Passenger numbers from aircraft to gate
    :return:
    """

    """
                        Start of Model definition
    """
    constraint_counter = 1

    ga = Model()
    x = dict()
    "Create x. lb is lower bound; ub is upper bound; vtype is variable type"
    for i in list(I.keys()):
        for j in list(K.keys()):
            x[i, j] = ga.addVar(lb=0, ub=1, vtype=GRB.BINARY, name=f'x_{i}{j}')


    w = dict()
    "Create omega, as these values can change during the optimisation process this should be a gurobi variable"
    for i in list(I.keys()):
        for k in list(K.keys()):
            for l in list(K.keys()):
                w[i, k, l] = ga.addVar(lb=0, vtype=GRB.INTEGER, name=f'w^{i}_{k}{l}')

    ga.update()
    """ Referenced in paper as equation (3). Forces plane to be ony assigned to one gate. Boolean condition is to check 
    if the flight is domestic, then domestic gates can be used, or international, then only domestic gates can be used. 
    """
    for i in list(I.keys()):
        K_gi = K_d if bool(I[i]) else K_i
        ga.addConstr(plane_assigned_to_only_one_gate(x, i, K_gi), name=f"C{constraint_counter}")
        constraint_counter += 1

    """ Referenced in paper as equation (4). Checks that for a certain time period, only one aircraft is assigned to a 
        domestic gate """
    for I_dt in T_D.values():
        for k in K_prime_d:
            ga.addConstr(one_aircraft_at_gate(x, I_dt, k), name=f"C{constraint_counter}")
            constraint_counter += 1

    """ Referenced in paper as equation (5). Checks that for a certain time period, only one aircraft is assigned to a 
        international gate """
    for I_it in T_I.values():
        for k in K_prime_i:
            ga.addConstr(one_aircraft_at_gate(x, I_it, k), name=f"C{constraint_counter}")
            constraint_counter += 1

    # """ Referenced in paper as equation (6). Checks that the number of aircraft in the apron is the same as the assigned
    #     number """
    # NA = find_number_in_apron(K_d, I_d, T_D) + find_number_in_apron(K_i, I_i, T_I)
    # ga.addConstr(number_of_aircraft_in_the_apron(x, K, I, NA), name=f"C{constraint_counter}")
    # constraint_counter += 1
    """ Equation (6) will be replaced by equation (13) and (14)"""
    for I_dt in T_D.values():
        if len(I_dt)-len(K_prime_d) > 0:
            ga.addConstr(number_of_aircraft_in_the_apron(x, I_dt, len(I_dt)-len(K_prime_d)), name=f"C{constraint_counter}")
            constraint_counter += 1
    """ Equation (14) """
    for I_it in T_I.values():
        if len(I_it)-len(K_prime_d) > 0:
            ga.addConstr(number_of_aircraft_in_the_apron(x, I_it, len(I_it)-len(K_prime_d)), name=f"C{constraint_counter}")
            constraint_counter += 1

    """ Referenced in paper as equation (10). """
    for i in list(I.keys()):
        K_gi = K_d if bool(I[i]) else K_i
        for k in list(K_gi):
            """ I think gurobi will optimise away all the non relevant values of k but look at the comment in 
            constr10_11 """
            ga.addConstr(transit_leaving(x, K, I, p, w, i, k), name=f"C{constraint_counter}")
            constraint_counter += 1

    """ Referenced in paper as equation (10). """
    for i in list(I.keys()):
        K_gi = K_d if I[i] else K_i
        for k in list(K):
            """I think gurobi will optimise away all the non relevant values of k but look at the comment in 
            constr10_11 """
            ga.addConstr(transit_coming(x, K_gi, I, p, w, i, k), name=f"C{constraint_counter}")
            constraint_counter += 1

    obj = LinExpr()
    for i in list(I.keys()):
        K_gi = K_d if I[i] else K_i
        for k in list(K_gi.keys()):
            for l in list(K_gi.keys()):
                obj += w[i, k, l] * K_gi[k][l]

            obj += (e[i] + f[i]) * K_gi[k]["e"] * x[i, k]

    ga.setObjective(obj, GRB.MINIMIZE)
    ga.update()
    ga.optimize()

    sol = ga.getVars()
    gate_names = list(K.keys())
    for i in I.keys():
        j = 0
        while(True):
            if sol[(i-1)*len(K.keys())+j].X >= 0.99:
                gate = gate_names[j]
                print(f"aircraft {i} assigned to gate {gate}")
                for l in gate_names:
                    print(f"\t with {ga.getVarByName(f'w^{i}_{gate}{l}').X} passengers going to gate {l}")
                    pass
                break
            j += 1
    ga.write('LP.lp')
