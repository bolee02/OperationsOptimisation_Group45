from gurobipy import Model, GRB, LinExpr
from constraints.constr3 import plane_assigned_to_only_one_gate
from constraints.constr4_5 import one_aircraft_at_gate, one_aircraft_at_gateV2
from constraints.constr6 import number_of_aircraft_in_the_apron
from constraints.constr10_11 import transit_leaving, transit_coming
from constraints.constr6_10and6_11 import same_fixed_gate


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
        K_gi = K_d if bool(I[i]) else K_i
        for j in list(K.keys()):
            x[i, j] = ga.addVar(lb=0, ub=1, vtype=GRB.BINARY, name=f'x_{i}{j}') if j in K_gi else 0



    w = dict()
    "Create omega, as these values can change during the optimisation process this should be a gurobi variable"
    for i in list(I.keys()):
        K_gi = K_d if bool(I[i]) else K_i
        for k in list(K.keys()):
            for l in list(K.keys()):
                w[i, k, l] = ga.addVar(lb=0, vtype=GRB.INTEGER, name=f'w^{i}_{k}{l}') if k in K_gi else 0

    ga.update()
    """ Referenced in paper as equation (3). Forces plane to be ony assigned to one gate. Boolean condition is to check 
    if the flight is domestic, then domestic gates can be used, or international, then only domestic gates can be used. 
    """
    for i in list(I.keys()):
        K_gi = K_d if bool(I[i]) else K_i
        ga.addConstr(plane_assigned_to_only_one_gate(x, i, K_gi), name=f"C1.{constraint_counter}")
        constraint_counter += 1

    """ Referenced in paper as equation (4). Checks that for a certain time period, only one aircraft is assigned to a 
        domestic gate """
    for I_dt in T_D.values():
        for k in K_prime_d:
            ga.addConstr(one_aircraft_at_gate(x, I_dt, k), name=f"C2.{constraint_counter}")
            constraint_counter += 1

    """ Referenced in paper as equation (5). Checks that for a certain time period, only one aircraft is assigned to a 
        international gate """
    for I_it in T_I.values():
        for k in K_prime_i:
            ga.addConstr(one_aircraft_at_gate(x, I_it, k), name=f"C3.{constraint_counter}")
            constraint_counter += 1

    # """ Referenced in paper as equation (6). Checks that the number of aircraft in the apron is the same as the assigned
    #     number """
    # NA = find_number_in_apron(K_d, I_d, T_D) + find_number_in_apron(K_i, I_i, T_I)
    # ga.addConstr(number_of_aircraft_in_the_apron(x, K, I, NA), name=f"C{constraint_counter}")
    # constraint_counter += 1
    """ Equation (6) will be replaced by equation (13) and (14)"""
    for I_dt in T_D.values():
        if len(I_dt)-len(K_prime_d) > 0:
            ga.addConstr(number_of_aircraft_in_the_apron(x, I_dt, len(I_dt)-len(K_prime_d)), name=f"C4.{constraint_counter}")
            constraint_counter += 1
    """ Equation (14) """
    for I_it in T_I.values():
        if len(I_it)-len(K_prime_i) > 0:
            ga.addConstr(number_of_aircraft_in_the_apron(x, I_it, len(I_it)-len(K_prime_i)), name=f"C5.{constraint_counter}")
            constraint_counter += 1

    """ Referenced in paper as equation (10). """
    for i in list(I.keys()):
        K_gi = K_d if bool(I[i]) else K_i
        for k in list(K_gi):
            """ I think gurobi will optimise away all the non relevant values of k but look at the comment in 
            constr10_11 """
            ga.addConstr(transit_leaving(x, K, I, p, w, i, k), name=f"C7.{constraint_counter}")
            constraint_counter += 1

    """ Referenced in paper as equation (10). """
    for i in list(I.keys()):
        K_gi = K_d if I[i] else K_i
        for k in list(K):
            """I think gurobi will optimise away all the non relevant values of k but look at the comment in 
            constr10_11 """
            ga.addConstr(transit_coming(x, K_gi, I, p, w, i, k), name=f"C8.{constraint_counter}")
            constraint_counter += 1

    obj = LinExpr()
    for i in list(I.keys()):
        K_gi = K_d if I[i] else K_i
        for k in list(K_gi.keys()):
            for l in list(K.keys()):
                obj += w[i, k, l] * K_gi[k][l]

            obj += (e[i] + f[i]) * K_gi[k]["e"] * x[i, k]

    ga.setObjective(obj, GRB.MINIMIZE)
    ga.update()
    ga.optimize()
    for i in I.keys():
        K_gi = K_d if I[i] else K_i
        for k in K_gi.keys():
            if ga.getVarByName(f"x_{i}{k}").X >= 0.99:
                print(f"aircraft {i} assigned to gate {k}")
                for l in K.keys():
                    print(f"\t with {ga.getVarByName(f'w^{i}_{k}{l}').X} passengers going to gate {l}")
                    pass
                break

    ga.write('LP.lp')
    ga.write('MPS.mps')
    constr = ga.getConstrs()
    return


def modelV2(I: dict, I_d: dict, I_i: dict, K: dict, K_d: dict, K_i: dict, t: dict, K_prime_d: dict,  K_prime_i: dict,
            p: dict, e: dict, f: dict):
    """
    :param I: All aircraft
    :param I_d: All domestic aircraft
    :param I_i: All international aircraft
    :param K: All gates
    :param K_d: All domestic gates
    :param K_i: All internation gates
    :param t: All time intervals
    :param K_prime_d:
    :param K_prime_i:
    :param p: Passenger numbers from aircraft to aircraft
    :param e: Passenger numbers from entrance to aircraft
    :param f: Passenger numbers from aircraft to exit
    :param w: Passenger numbers from aircraft to gate
    :return:
    """

    def overlapping_arriving_aircraft(T: dict, I: dict):
        T_a = dict()
        for t in T.keys():
            I_a_t = []
            for i in I.keys():
                if I[i][t]:
                    I_a_t += [i]
            if len(I_a_t) > 1:
                T_a[t] = I_a_t
        return T_a

    def overlapping_departing_aircraft(T: dict, I: dict):
        T_d = dict()
        for t in T.keys():
            I_d_t = []
            for i in I.keys():
                if t == max(T.keys()) and I[i][t]:
                    I_d_t += [i]
                elif I[i][t] and not I[i][t + 1]:
                    I_d_t += [i]
            if len(I_d_t) > 1:
                T_d[t] = I_d_t
        return T_d

    T_a_D = overlapping_arriving_aircraft(t, I_d)
    T_a_I = overlapping_arriving_aircraft(t, I_i)
    T_d_D = overlapping_departing_aircraft(t, I_d)
    T_d_I = overlapping_departing_aircraft(t, I_i)

    """
                        Start of Model definition
    """
    constraint_counter = 1

    ga = Model()
    x = dict()
    z = dict()
    "Create x and z. lb is lower bound; ub is upper bound; vtype is variable type"
    for i in list(I.keys()):
        K_gi = K_d if bool(I[i]) else K_i
        for j in list(K.keys()):
            x[i, j] = ga.addVar(lb=0, ub=1, vtype=GRB.BINARY, name=f'x_{i}{j}') if j in K_gi else 0
            z[i, j] = ga.addVar(lb=0, ub=1, vtype=GRB.BINARY, name=f'z_{i}{j}') if j in K_gi else 0

    w = dict()
    "Create omega"
    for i in list(I.keys()):
        K_gi = K_d if bool(I[i]) else K_i
        for k in list(K.keys()):
            for l in list(K.keys()):
                w[i, k, l] = ga.addVar(lb=0, vtype=GRB.INTEGER, name=f'w^{i}_{k}{l}') if k in K_gi else 0

    ga.update()
    """ Referenced in report as equation (6.2). Forces plane to be ony assigned to one gate. Boolean condition is to 
    same as defined in old model. 
    """
    for i in list(I.keys()):
        K_gi = K_d if bool(I[i]) else K_i
        ga.addConstr(plane_assigned_to_only_one_gate(x, i, K_gi), name=f"C{constraint_counter}A/C2OneGate")
        constraint_counter += 1

    """ Referenced in report as equation (6.3). Forces plane to be ony assigned to one gate. Boolean condition is to 
    same as defined in old model. 
    """
    for i in list(I.keys()):
        K_gi = K_d if bool(I[i]) else K_i
        ga.addConstr(plane_assigned_to_only_one_gate(z, i, K_gi), name=f"C{constraint_counter}")
        constraint_counter += 1

    """ Referenced in report as equation (6.4). Checks that for a certain time period, only one aircraft is assigned to a 
        domestic gate """
    for I_a_dt in T_a_D.values():
        for k in K_prime_d:
            ga.addConstr(one_aircraft_at_gate(x, I_a_dt, k), name=f"C{constraint_counter}")
            constraint_counter += 1

    """ Referenced in report as equation (6.5). Checks that for a certain time period, only one aircraft is assigned to a 
        international gate """
    for I_a_it in T_a_I.values():
        for k in K_prime_i:
            ga.addConstr(one_aircraft_at_gate(x, I_a_it, k), name=f"C{constraint_counter}")
            constraint_counter += 1

    """ Referenced in report as equation (6.6). Checks that for the departing time period, that only one aircraft is 
    assigned to a domestic gate """
    for I_d_dt in T_d_D.values():
        for k in K_prime_d:
            ga.addConstr(one_aircraft_at_gate(z, I_d_dt, k), name=f"C{constraint_counter}")
            constraint_counter += 1

    """ Referenced in report as equation (6.7). Checks that for the departing time period, that only one aircraft is 
    assigned to a domestic gate """
    for I_d_it in T_d_I.values():
        for k in K_prime_i:
            ga.addConstr(one_aircraft_at_gate(z, I_d_it, k), name=f"C{constraint_counter}")
            constraint_counter += 1

    """ Referenced in the report as equation (6.8). """
    for i in list(I.keys()):
        K_gi = K_d if bool(I[i]) else K_i
        for k in list(K_gi):
            ga.addConstr(transit_leaving(x, K, I, p, w, i, k), name=f"C{constraint_counter}")
            constraint_counter += 1

    """ Referenced in the report as equation (6.9). """
    for i in list(I.keys()):
        K_gi = K_d if I[i] else K_i
        for k in list(K):
            ga.addConstr(transit_coming(z, K_gi, I, p, w, i, k), name=f"C{constraint_counter}")
            constraint_counter += 1

    """ Referenced in the report a equation (6.12). Forces same departing fixed gate as arriving fixed gate"""
    for i in list(I.keys()):
        K_prime_gi = K_prime_d if I[i] else K_prime_i
        for k in K_prime_gi:
            ga.addConstr(same_fixed_gate(x[i, "a"], z[i, k], x[i, k]))

    obj = LinExpr()
    for i in list(I.keys()):
        K_gi = K_d if I[i] else K_i
        for k in list(K_gi.keys()):
            obj += (e[i] * x[i, k] + f[i] * z[i, k]) * K_gi[k]["e"]

            for l in list(K.keys()):
                obj += w[i, k, l] * K_gi[k][l]


    ga.setObjective(obj, GRB.MINIMIZE)
    ga.update()
    ga.optimize()

    for i in I.keys():
        K_gi = K_d if I[i] else K_i
        for k_1 in K_gi.keys():
            if ga.getVarByName(f"x_{i}{k_1}").X >= 0.99:
                break
        for k_2 in K_gi.keys():
            if ga.getVarByName(f"z_{i}{k_2}").X >= 0.99:
                print(f"aircraft {i} assigned to arrive at gate {k_1} and depart from gate {k_2}")
                for l in K.keys():
                    print(f"\t with {ga.getVarByName(f'w^{i}_{k_1}{l}').X} passengers going to gate {l}")
                    pass
                break

    ga.write('LP.lp')
    ga.write('MPS.mps')
    constr = ga.getConstrs()
    return
