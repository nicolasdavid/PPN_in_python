import ppl


class Vertex:
    """
       This class represents the vertex of a (Parametric) Petri Net : Places and Transitions.
    """

    def __init__(self, id):
        self.id = id
        self.post = []
        self.pre = []

    def get_id(self):
        return self.id

    def get_pre(self):
        return self.pre

    def get_post(self):
        return self.post

    def add_pre(self, arc):
        self.pre.append(arc)

    def add_post(self, arc):
        self.post.append(arc)

    def __str__(self):
        return str(self.id)


class Place(Vertex):
    def __init__(self, id, tokens=ppl.Linear_Expression(0)):
        Vertex.__init__(self, id)
        self.tokens = tokens

    def get_tokens(self):
        return self.tokens

    def set_tokens(self, amount):
        self.tokens = amount

    def add_tokens(self, amount):
        self.tokens += amount

    def consume_tokens(self, amount):
        self.tokens -= amount

    def is_transition(self):
        return False


class Transition(Vertex):
    def is_transition(self):
        return True

    def is_parametric_pre(self):
        return any(arc.is_parametric() for arc in self.pre)

    def is_parametric_post(self):
        return any(arc.is_parametric() for arc in self.post)

    def is_parametric(self):
        return self.is_parametric_pre() or self.is_parametric_post()

    def fire(self):
        for arc in self.pre:
            arc.consume()
        for arc in self.post:
            arc.generate()

    def get_firing_constraint(self):
        cs = ppl.Constraint_System()
        for arc in self.pre:
            cs.insert(arc.get_firing_constraint())
        return cs

    def get_param_present_pre(self, params):
        s = set()
        for arc in self.get_pre():
            s.update(arc.get_param_present(params))
        return s

    def get_param_present_post(self, params):
        s = set()
        for arc in self.get_post():
            s.update(arc.get_param_present(params))
        return s