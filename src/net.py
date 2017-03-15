from src.vertex import *
from src.ppl_wrapper import *
from src.arc import *
from src.marking import *

import ppl
import os
from lxml import etree

class Net:
    """
    Class that describes a Parametric Petri Net.
    """
    def __init__(self, id, nbP, nbT, nbPar):
        self.id = id
        self.places = [Place("p" + str(i)) for i in range(nbP)]
        self.transitions = [Transition("t" + str(i)) for i in range(nbT)]
        self.params = [Parameter(i) for i in range(nbPar)]
        self.constraints = ppl.Constraint_System()
        for param in self.params:
            self.constraints.insert(param >= 0)

    def evaluate(self, val):
        """
        Evaluate a Parametric Petri Net by replacing its parameters by the values in the list dictionary.
        Val is not mandatory to specify all parameters of the net.
        Notice that this evaluation works fine with linear combination of parameters.
        """
        assert len(val) <= len(self.params)
        val_comb = [0 for i in range(len(self.params))]
        for i in range(len(self.params)) :
            value = val.get(i,"unassigned")
            if not(value == "unassigned"):
                val_comb[i] = ppl.Linear_Expression(value - self.params[i])
        for t in self.transitions:
                for arc in t.getPre() :
                    if(arc.is_parametric()):
                        coeff = [arc.weight.coefficient(self.params[i]) for i in range(len(self.params))]
                        for i in range(len(self.params)) :
                            arc.weight = arc.weight +coeff[i]*val_comb[i]
                for arc in t.getPost() :
                    if (arc.is_parametric()):
                        coeff = [arc.weight.coefficient(self.params[i]) for i in range(len(self.params))]
                        for i in range(len(self.params)) :
                            arc.weight = arc.weight +coeff[i]*val_comb[i]

    def __str__(self):
        return "PPN %s:\n list of places: %s\n list of transitions: %s\n list of parameters: %s\n list of constraints: %s\n" % (
        self.id, ", ".join(map(str, self.places)), ", ".join(map(str, self.transitions)),
        ", ".join(map(str, self.params)), " && ".join(map(str, list(self.constraints))))

    def is_parametric(self):
        """
        Test if a net has at least one parametric arc i.e. if it is not a classic PN
        return:
            boolean
        """
        return any(t.is_parametric() for t in self.transitions)

    def is_pre_parametric(self):
        """
        Test if a net has only parameters on input arc i.e. if it is a preT-PPN
        return:
            boolean
        """
        return any(t.isParametricPre() for t in self.transitions) and all(not t.isParametricPost() for t in self.transitions)

    def is_post_parametric(self):
        """
        Test if a net has only parameters on output arc i.e. if it is a postT-PPN
        return:
            boolean
        """
        return any(t.isParametricPost() for t in self.transitions) and all(not t.isParametricPre() for t in self.transitions)

    def is_distinct_parametric(self):
        """
        Test if a net has different parameters on input vs output arc i.e. if it is a distinctT-PPN.
        Note that a preT-PPN or a postT-PPN is a particular distinctT-PPN.
        To test if a net is strictly a distinctT-PPN and not a more precise subclass,
        we should return :
            return len(setPre & setPost) == 0 #and len(setPre) != 0 and len(setPost) != 0
        return:
            boolean
        """
        setPre = set()
        setPost = set()
        for t in self.transitions :
            if t.isParametricPre() :
                setPre.update(t.get_param_present_pre(self.params))
            if t.isParametricPost() :
                setPost.update(t.get_param_present_post(self.params))
        return len(setPre & setPost) == 0 #and len(setPre) != 0 and len(setPost) != 0

    def get_type_of_net(self):
        """
        Get the syntactical class of a PPN among :
            T-PPN  <-- distinctT-PPN <-- {preT-PPN} OR  {postT-PPN <--(P-PPN)} <--  PN
        Note that a parametric initial marking (P-PPN) can be easily translated into a postT-PPN.
        We therefore do not test this subclass.
        return:
            string
        """
        if not self.is_parametric():
            return "Petri Net"
        elif self.is_pre_parametric():
            return "preT-PPN"
        elif self.is_post_parametric():
            return "postT-PPN"
        elif self.is_distinct_parametric():
            return "distinctT-PPN"
        else:
            return "T-PPN"

    def marking(self):
        """
        return a dict describing the current marking of the net.
        """
        tokens = {x: x.getTokens() for x in self.places}
        return tokens

    def display_marking(self):
        """
        return a string describing the current marking of the net.
        """
        l = map(lambda x: x.getTokens(), self.places)
        return ",".join(map(str, l))

    def update_constraint_system(self):
        """
        Update the constraint system of the net by imposing that the current marking must be positive.
        """
        for p in self.places:
            self.constraints.insert(p.getTokens() >= 0)

    def fire(self, t):
        """
        Fire a transition in the net and update the tokens of the place of the net.
        """
        assert self.is_enabled(t)
        t.fire()
        self.update_constraint_system()

    def is_enabled(self, t):
        """
        Ask whether a transition can be fired or not.
        """
        context = self.constraints
        for c in list(t.getFiringConstraint()):
            context.insert(c)
        #DO WITH OK()
        poly = ppl.NNC_Polyhedron(context)
        return not poly.is_empty()

    def export_to_dot(self):
        """
        Generate a dot file description of the Petri Net.
        """
        name = "exported_net_%s" % (self.id)
        file = open( "export/" + name + ".dot", "w")
        file.write("digraph {\n")
        for t in self.transitions:
            for arc in t.pre:
                file.write("%s -> %s[label=\"%s\"]\n" % (arc.input.id, arc.output.id, str(arc.weight)))
            for arc in t.post:
                file.write("%s -> %s[label=\"%s\"]\n" % (arc.input.id, arc.output.id, str(arc.weight)))
        for p in self.places:
            file.write("%s[label=\"%s\"]\n" % (p.id, str(p.tokens)))
        for t in self.transitions:
            file.write("%s[shape=box,color=lightblue2,label=\"%s\"]\n" % (t.id, t.id))
        file.write("}")
        file.close()
        command = "dot -Tpng export/%s.dot > export/%s.png" % (name, name)
        os.system(command)

    def formal_marking(self):
        #TODO : warning for comparisons...
        # for the moment only integer marking...
        # otherwise only takes the inhomogeneous part of the linear expr
        m = Marking(len(self.places))
        m.set_value([p.getTokens() for p in self.places])
        return m

    def get_pre_matrix(self):
        return [[t.get_coeff_pre(p) for p in self.places] for t in self.transitions]

    def get_post_matrix(self):
        return [[t.get_coeff_post(p) for p in self.places] for t in self.transitions]

class NetFromRomeoXML(Net):
    """
    Class that describes a Parametric Petri Net constructed from a Romeo Model.
    See :
        http://romeo.rts-software.org/
    """
    def __init__(self, fileName, nbParamToAdd):
        tree = etree.parse("xml/%s.xml" % fileName)
        nbPlaces = 0
        nbTransitions = 0
        for p in tree.xpath("/TPN/place"):
            nbPlaces += 1
        for t in tree.xpath("/TPN/transition"):
            nbTransitions += 1
        super().__init__(fileName,nbPlaces, nbTransitions, nbParamToAdd)
        self.arcs = []
        i = 0
        o = 0
        for arc in tree.xpath("/TPN/arc"):
            if arc.get("type") == "TransitionPlace":
                self.arcs.append(Arc("i%s" % i, ppl.Linear_Expression(int(arc.get("weight"))),
                                self.transitions[int(arc.get("transition")) - 1],
                                self.places[int(arc.get("place")) - 1]))
                i += 1
            elif arc.get("type") == "PlaceTransition":
                self.arcs.append(Arc("o%s" % o, ppl.Linear_Expression(int(arc.get("weight"))),
                                self.places[int(arc.get("place")) - 1],
                                self.transitions[int(arc.get("transition")) - 1]))
                o += 1
            else:
                print("Error")

        for p in tree.xpath("/TPN/place"):
            self.places[int(p.get("id")) - 1].addTokens(ppl.Linear_Expression(int(p.get("initialMarking"))))