import ppl

class Parameter (ppl.Variable):
    def __hash__(self):
    # Use only one variable per dimension to avoid conflicts
        return self.id()