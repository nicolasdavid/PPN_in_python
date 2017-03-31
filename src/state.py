from src.net import *
from src.ppl_wrapper import *

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

    def __eq__(self, other):
        """
        Compare if a marking is greater than another. Note that we will only compare marking from a same run.
        Thus, self.poly is necessarily included in other.poly.
        Nevertheless, we need to ensure that self.marking == other.marking for every valuation stafisfying self.poly.
        """
        #TODO assert same net ?
        poly_copy = ppl.NNC_Polyhedron(self.poly)
        for j in range(len(self.marking)):
            poly_copy.add_constraint(self.marking[j] == other.marking[j])
        return self.poly.contains(poly_copy)

    def __ge__(self, other):
        """
        Compare if a marking is greater than another. Note that we will only compare marking from a same run.
        Thus, self.poly is necessarily included in other.poly.
        Nevertheless, we need to ensure that self.marking > other.marking for every valuation stafifying self.poly.
        """
        #TODO assert same net ?
        poly_copy = ppl.NNC_Polyhedron(self.poly)
        for j in range(len(self.marking)):
            poly_copy.add_constraint(self.marking[j] >= other.marking[j])
        return self.poly.contains(poly_copy)

    def __gt__(self, other):
        """
        Compare if a marking is greater than another. Note that we will only compare marking from a same run.
        Thus, self.poly is necessarily included in other.poly.
        Nevertheless, we need to ensure that self.marking > other.marking for every valuation stafifying self.poly.
        """
        #TODO assert same net ?
        return self>=other and not self == other

    def is_enabled(self, t):
        """
        Ask whether a transition from self.net can be fired or not from self.
        """
        assert t in self.net.transitions
        i = self.net.transitions.index(t)
        poly_copy = ppl.NNC_Polyhedron(self.poly)
        for j in range(len(self.marking)):
            poly_copy.add_constraint(self.marking[j] >= self.net.Pre[i][j])
        return not poly_copy.is_empty()

    def get_enabled_transitions(self):
        return [t for t in self.net.transitions if self.is_enabled(t)]

    def fire(self, t):
        assert self.is_enabled(t)
        i = self.net.transitions.index(t)
        for j in range(len(self.marking)):
            self.poly.add_constraint(self.marking[j] >= self.net.Pre[i][j])
            self.marking[j] = self.marking[j] - self.net.Pre[i][j] + self.net.Post[i][j]
            self.poly.add_constraint(self.marking[j] >= LinearExpressionExtended(0))