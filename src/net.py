class Net:
    """
    Class that describes a parametric Petri net
    """
    def __init__(self, id):
        self.id = id

    def __str__(self):
        return "PPN %s" %(self.id)