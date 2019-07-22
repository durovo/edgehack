class State:
    def __init__(self, direction, constraints, order,isStateReached):
        self.constraints = constraints
        self.currentPosition = None
        self.previousPosition = None
        self.direction = direction
        self.order = order 
        self.isStateReached = isStateReached
    
    def areConstraintsMet(self):
        return all(constraint.evaluate() for constraint in self.constraints) and self.isCorrectDirection()
    
    def updatePosition(self, data):
        self.previousPosition = self.currentPosition
        self.currentPosition = data

    def isCorrectDirection(self):
        return (self.currentPosition - self.previousPosition) * self.direction > 0


