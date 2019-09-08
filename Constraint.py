
class Constraint:
    def __init__(self, checker, toleranceExceeded):
        self.checker = checker
        self.toleranceExceeded = toleranceExceeded

    def evaluate(self):
        if self.checker():
            return True
        else:
            return self.checker("raiseError")

    def checkTolerance(self):
        return self.toleranceExceeded()