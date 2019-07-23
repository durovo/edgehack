
class Constraint:
    def __init__(self, checker):
        self.checker = checker

    def evaluate(self):
        if self.checker():
            return True
        else:
            return self.checker("raiseError")