from src.vertex import *
from src.arc import *
from src.ppl_wrapper import *

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
        TODO : 
            Detect if the valuation generates negative markings inside the places and thus forbid it if necessary
        """
        assert len(val) <= len(self.params)
        val_comb = [0 for i in range(len(self.params))]
        for i in range(len(self.params)) :
            value = val.get(i,"unassigned")
            if value != "unassigned":
                val_comb[i] = ppl.Linear_Expression(value - self.params[i])
        for t in self.transitions:
                for arc in t.get_pre() :
                    if arc.is_parametric():
                        coeff = [arc.weight.value.coefficient(self.params[i]) for i in range(len(self.params))]
                        for i in range(len(self.params)):
                            arc.weight.value = arc.weight.value + coeff[i]*val_comb[i]
                for arc in t.get_post() :
                    if arc.is_parametric():
                        coeff = [arc.weight.value.coefficient(self.params[i]) for i in range(len(self.params))]
                        for i in range(len(self.params)):
                            arc.weight.value = arc.weight.value + coeff[i]*val_comb[i]
        for p in self.places:
            if p.is_marking_parameterized():
                coeff = [p.tokens.value.coefficient(self.params[i]) for i in range(len(self.params))]
                for i in range(len(self.params)):
                    p.tokens.value = arc.weight.value + coeff[i] * val_comb[i]

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
        return any(t.is_parametric_pre() for t in self.transitions) and all(not t.is_parametric_post() for t in self.transitions)

    def is_post_parametric(self):
        """
        Test if a net has only parameters on output arc i.e. if it is a postT-PPN
        return:
            boolean
        """
        return any(t.is_parametric_post() for t in self.transitions) and all(not t.is_parametric_pre() for t in self.transitions)

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
            if t.is_parametric_pre() :
                setPre.update(t.get_param_present_pre(self.params))
            if t.is_parametric_post() :
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
        return a list describing the current marking of the net.
        """
        tokens = [x.get_tokens() for x in self.places]
        return tokens

    def display_marking(self):
        """
        return a string describing the current marking of the net.
        """
        l = map(lambda x: x.get_tokens(), self.places)
        return ",".join(map(str, l))

    def update_constraint_system(self):
        """
        Update the constraint system of the net by imposing that the current marking must be positive.
        """
        for p in self.places:
            self.constraints.insert(p.tokens >= LinearExpressionExtended(0))

    def fire(self, t):
        """
        Fire a transition in the net and update the tokens of the place of the net.
        """
        assert self.is_enabled(t)
        for c in list(t.get_firing_constraint()):
            self.constraints.insert(c)
        t.fire()
        self.update_constraint_system()

    def is_enabled(self, t):
        """
        Ask whether a transition can be fired or not.
        """
        context = ppl.Constraint_System(self.constraints)
        for c in list(t.get_firing_constraint()):
            context.insert(c)
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

    def compute_pre_matrix(self):
        return [[t.get_pre_vector(p) for p in self.places] for t in self.transitions]

    def compute_post_matrix(self):
        return [[t.get_post_vector(p) for p in self.places] for t in self.transitions]

    def get_enabled_transitions(self):
        return [t for t in self.transitions if self.is_enabled(t)]

    def execute(self):
        """
        User interactive execution of the net. 
        Warning : the initial marking is lost during the execution.
        """
        m = self.marking()
        enabled = self.get_enabled_transitions()
        exec = True
        while(exec and len(enabled)>0):
            print("chose a transition among %s" %enabled)
            while True:
                try:
                    i = int(input("Fire t_i with i = ? (integer)..."))
                except ValueError:
                    print("Sorry, we need an integer here.")
                    # indice not parsed, redo the loop
                    continue
                else:
                    # indice was successfully parsed, exit loop
                    break
            past = m
            self.fire(self.transitions[i])
            m = self.marking()
            print("%s -- t%s --> %s" % (str(past), str(i), str(m)))
            while True:
                answer = input("Continue ? (Y/N)")
                if answer.upper()[0] == "N":
                    exec = False
                    break
                elif answer.upper()[0] == "Y":
                    exec = True
                    break
                else:
                    continue


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
                self.arcs.append(Arc("i%s" % i, LinearExpressionExtended(int(arc.get("weight"))),
                                self.transitions[int(arc.get("transition")) - 1],
                                self.places[int(arc.get("place")) - 1]))
                i += 1
            elif arc.get("type") == "PlaceTransition":
                self.arcs.append(Arc("o%s" % o, LinearExpressionExtended(int(arc.get("weight"))),
                                self.places[int(arc.get("place")) - 1],
                                self.transitions[int(arc.get("transition")) - 1]))
                o += 1
            else:
                print("Error")

        for p in tree.xpath("/TPN/place"):
            self.places[int(p.get("id")) - 1].add_tokens(LinearExpressionExtended(int(p.get("initialMarking"))))

