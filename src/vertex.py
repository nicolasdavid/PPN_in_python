import ppl


class Vertex:
    """
       This class represents the vertex of a (Parametric) Petri Net : Places and Transitions.
    """

    def __init__(self, id):
        self.id = id
        self.post = []
        self.pre = []

    def getId(self):
        return self.id

    def getPre(self):
        return self.pre

    def getPost(self):
        return self.post

    def addPre(self, arc):
        self.pre.append(arc)

    def addPost(self, arc):
        self.post.append(arc)

    def __str__(self):
        return str(self.id)


class Place(Vertex):
    def __init__(self, id, tokens=ppl.Linear_Expression(0)):
        Vertex.__init__(self, id)
        self.tokens = tokens

    def getTokens(self):
        return self.tokens

    def setTokens(self, amount):
        self.tokens = amount

    def addTokens(self, amount):
        self.tokens += amount

    def consumeTokens(self, amount):
        self.tokens -= amount

    def isTransition(self):
        return False


class Transition(Vertex):
    def isTransition(self):
        return True

    def isParametricPre(self):
        return any(arc.is_parametric() for arc in self.pre)

    def isParametricPost(self):
        return any(arc.is_parametric() for arc in self.post)

    def is_parametric(self):
        return self.isParametricPre() or self.isParametricPost()

    def fire(self):
        for arc in self.pre:
            arc.consume()
        for arc in self.post:
            arc.generate()

    def getFiringConstraint(self):
        cs = ppl.Constraint_System()
        for arc in self.pre:
            cs.insert(arc.get_firing_constraint())
        return cs

    def get_param_present_pre(self, params):
        s = set()
        for arc in self.getPre():
            s.update(arc.get_param_present(params))
        return s

    def get_param_present_post(self, params):
        s = set()
        for arc in self.getPost():
            s.update(arc.get_param_present(params))
        return s

    def get_coeff_pre(self, place):
        for arc in self.pre:
            if arc.input == place:
                return arc.weight
        return 0

    def get_coeff_post(self, place):
        for arc in self.post:
            if arc.output == place:
                return arc.weight
        return 0