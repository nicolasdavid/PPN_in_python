import numpy

class Marking:

    def __init__(self,size):
        self.value = [0 for i in range(size)]
        self.omega = [False for i in range(size)]

    def set_value(self, list):
        self.value = list

    def set_omega(self, list):
        self.omega = list

    def keep_integer_value(self, omega):
        intVal = [i for (i, b) in zip(self.value, omega) if b]
        return intVal

    def __str__(self):
        return str([u"\u03C9" if b else i for (i, b) in zip(self.value, self.omega)])

    def __eq__(self, other):
        return self.omega == other.omega and self.keep_integer_value(other.omega) == other.keep_integer_value(other.omega)

    def __lt__(self, other):
        if self.omega < other.omega:
            return self.keep_integer_value(other.omega) <= other.keep_integer_value(other.omega)
        elif self.omega == other.omega:
            return self.keep_integer_value(other.omega) < other.keep_integer_value(other.omega)
        else:
            return False

    def __le__(self, other):
        return self == other or self < other

    def __sub__(self, other):
        """
        Warning : add a marking and a list of value
        Param :
            other is a list of value
        Return :
            a new marking
        """
        l = len(self.value)
        m = Marking(l)
        m.set_value([self.value[i]-other[i] for i in range(l)])
        m.set_omega(self.omega)
        return m

   # def __add__(self, other):

