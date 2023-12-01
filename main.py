from gurobipy import GRB.INFINITY

#set of domestic gates
K_d = {
    "1":{"1":0, "2":50, "3":100, "4":150, "e":50},
    "2":{"1":50, "2":0, "3":50, "4":100, "e":50},
    "3":{"1":100, "2":50, "3":0, "4":50, "e":50},
    "4":{"1":150, "2":100, "3":50, "4":0, "e":50},
    "5":{"1":GRB.INFINITY, "2":GRB.INFINITY, "3":GRB.INFINITY, "4":GRB.INFINITY, "e":GRB.INFINITY} #apron
}

