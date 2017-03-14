import ppl

class Parameter (ppl.Variable):
    """
    This class allows to consider sets of Parameter which is not allowed using ppl.Variable

    Example:
        v = Parameter(0)
        print(v)
        print(v.__hash__())
        expr = ppl.Linear_Expression(v + 2)

        listVars = set()
        listVars.add(Parameter(0))
    """
    def __hash__(self):
    # Use only one variable per dimension to avoid conflicts
        return self.id()