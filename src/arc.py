class Arc:
    def __init__(self, id, weight, input, output):
        assert (input.is_transition() != output.is_transition()), "Error: same input and output class"
        self.id = id
        self.weight = weight
        self.input = input
        self.output = output
        self.input.add_post(self)
        self.output.add_pre(self)

    def __str__(self):
        return str(self.id) + ": arc from " + str(self.input) + " to " + str(self.output) + " of weight " + str(
            self.weight)

    def is_input_arc(self):
        return self.output.is_transition()

    def is_output_arc(self):
        return self.input.is_transition()

    def generate(self):
        assert (self.is_output_arc())
        self.output.add_tokens(self.weight)

    def consume(self):
        assert (self.is_input_arc())
        self.input.consume_tokens(self.weight)

    def get_firing_constraint(self):
        assert (self.is_input_arc())
        return self.input.get_tokens() >= self.weight

    def is_parametric(self):
        return not self.weight.all_homogeneous_terms_are_zero()

    def get_param_present(self, params):
        s = set()
        for p in params:
            if self.weight.coefficient(p) != 0:
                s.add(p)
        return s