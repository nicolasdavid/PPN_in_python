class Arc:
    def __init__(self, id, weight, input, output):
        assert (input.isTransition() != output.isTransition()), "Error: same input and output class"
        self.id = id
        self.weight = weight
        self.input = input
        self.output = output
        self.input.addPost(self)
        self.output.addPre(self)

    def __str__(self):
        return str(self.id) + ": arc from " + str(self.input) + " to " + str(self.output) + " of weight " + str(
            self.weight)

    def is_input_arc(self):
        return self.output.isTransition()

    def is_output_arc(self):
        return self.input.isTransition()

    def generate(self):
        assert (self.is_output_arc())
        self.output.addTokens(self.weight)

    def consume(self):
        assert (self.is_input_arc())
        self.input.consumeTokens(self.weight)

    def get_firing_constraint(self):
        assert (self.is_input_arc())
        return self.input.getTokens() >= self.weight

    def is_parametric(self):
        return not self.weight.all_homogeneous_terms_are_zero()

    def get_param_present(self, params):
        s = set()
        for p in params:
            if self.weight.coefficient(p) != 0:
                s.add(p)
        return s