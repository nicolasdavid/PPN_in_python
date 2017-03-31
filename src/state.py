from src.net import *

import ppl



class State:

    def __init__(self, id, net, marking=None, constraints=None):
        self.id = id
        self.net = net
        if marking==None:
            self.marking = net.marking()[:]
        else:
            self.marking = marking[:]
        if marking == None:
            self.poly = ppl.NNC_Polyhedron(net.constraints)
        else:
            self.poly = ppl.NNC_Polyhedron(constraints)

    def __str__(self):
        return "State %s:\nm=%s\nsatisfying: %s" %(str(self.id), str(self.marking),str(self.poly.minimized_constraints()))



