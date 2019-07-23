class State:
    def __init__(self, direction, constraints, order, isStateReached, name):
        self.constraints = constraints
        self.currentPosition = None
        self.previousPosition = None
        self.direction = direction
        self.order = order 
        self.isStateReached = isStateReached
        self.name = name
    
    def areConstraintsMet(self):
        return all(constraint.evaluate() for constraint in self.constraints) and self.isCorrectDirection()
    
    def updatePosition(self, data):
        self.previousPosition = self.currentPosition
        self.currentPosition = data

    def isCorrectDirection(self):
        if self.previousPosition is None or self.currentPosition is None:
            return True
        return (self.currentPosition - self.previousPosition) * self.direction >= 0


