class State:
    def __init__(self, constraints, order, isStateReached, name):
        self.constraints = constraints
        self.currentPosition = None
        self.previousPosition = None
        self.order = order 
        self.isStateReached = isStateReached
        self.name = name
        self.constraintViolations = 0
    
    def areConstraintsMet(self):
        return all(constraint.evaluate() for constraint in self.constraints)
    
    def updatePosition(self, data):
        self.previousPosition = self.currentPosition
        self.currentPosition = data



