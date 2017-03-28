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


class LinearExpressionExtended:
    """
    Extend Linear Expression with omega.

    Note:
        To be consistent, each comparison operator returns a ppl.Constraint
    """

    def __init__(self, value=0, infinite=False):
        self.value = ppl.Linear_Expression(value)
        self.infinite = infinite

    def __str__(self):
        if self.infinite:
            return 	u"\u03C9"
        else:
            return str(self.value)

    def __repr__(self):
        return str(self)

    def __add__(self, other):
        infinite = self.infinite or other.infinite
        value = self.value + other.value
        return LinearExpressionExtended(value=value, infinite=infinite)

    def __sub__(self, other):
        try:
            if(other.infinite):
                raise ValueError("the element to substract is equal to %s" %u"\u03C9")
        except ValueError:
                print("The substraction cannot be done. (the second member may be equal to %s)" %u"\u03C9")
        else:
            infinite = self.infinite
            value = self.value - other.value
            return LinearExpressionExtended(value=value, infinite=infinite)

    def __mul__(self, other):
        """
        TODO : check
        multiply an extended linear expression with a scalar.
        Exception if the linear expression is equal to omega.
        """
        try:
            b = int(other)
            if self.infinite:
                raise ValueError("one element is equal to %s" %u"\u03C9")
        except ValueError:
            print("The multiplication cannot be done. (one member may be equal to %s)" %u"\u03C9")
        except TypeError:
            print("The second member should be a scalar")
        else:
            value = self.value * other
            return LinearExpressionExtended(value=value)

    def __eq__(self, other):
        if self.infinite and other.infinite:
            return ppl.Linear_Expression(1) >= 0
        elif (not self.infinite) and (not other.infinite):
            return self.value == other.value
        else:
            return ppl.Linear_Expression(-1) >= 0
        return cs

    def __le__(self, other):
        if other.infinite:
            return ppl.Linear_Expression(1) >= 0
        else:
            if self.infinite:
                return ppl.Linear_Expression(-1) >= 0
            else:
                return self.value <= other.value
        return cs

    def __lt__(self, other):
        if self.infinite:
            return ppl.Linear_Expression(-1) >= 0
        elif other.infinite and not self.infinite:
            return ppl.Linear_Expression(1) >= 0
        else:
            return self.value < other.value
        return cs

    def __gt__(self, other):
        return other < self

    def __ge__(self, other):
        return other <= self

