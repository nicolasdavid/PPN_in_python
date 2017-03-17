class IntegerExtended:

    def __init__(self, value=0, infinite=False):
        self.value = value
        self.infinite = infinite

    def __str__(self):
        if self.infinite:
            return 	u"\u03C9"
        else:
            return str(self.value)

    def __add__(self, other):
        infinite = self.infinite or other.infinite
        value = self.value + other.value
        return IntegerExtended(value=value, infinite=infinite)

    def __sub__(self, other):
        try:
            if(other.infinite):
                raise ValueError("the element to substract is equal to %s" %u"\u03C9")
        except ValueError:
                print("The substraction cannot be done. (the second member may be equal to %s)" %u"\u03C9")
        else:
            infinite = self.infinite or other.infinite
            value = self.value - other.value
            return IntegerExtended(value=value, infinite=infinite)

    def __eq__(self, other):
        if self.infinite and other.infinite:
            return True
        elif (not self.infinite) and (not other.infinite):
            return self.value == other.value
        else:
            return False

    def __le__(self, other):
        if self.infinite and not other.infinite:
            return False
        elif other.infinite and not self.infinite:
            return True
        elif self.infinite and other.infinite:
            return True
        else:
            return self.value <= other.value

    def __lt__(self, other):
        if self.infinite and not other.infinite:
            return False
        elif other.infinite and not self.infinite:
            return True
        elif self.infinite and other.infinite:
            return False
        else:
            return self.value < other.value

    def __gt__(self, other):
        return other < self

    def __ge__(self, other):
        return other <= self



