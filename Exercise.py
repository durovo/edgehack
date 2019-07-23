class Exercise:
    def __init__(self, statesList, name = None):
        self.stateFlow = statesList
        self.currentState = None
        self.nextState = statesList[0]
        self.name = name
        self.reps  = -1

    def calculateNextState(self):
        return self.stateFlow[(self.currentState.order + 1) % len(self.stateFlow)]

    def transitionToNextState(self):
        self.currentState = self.nextState
        self.nextState = self.calculateNextState()

    def continueExercise(self, data):
        if self.currentState is None:
            if self.nextState.isStateReached():
                self.transitionToNextState()
                if self.currentState.order == 0:
                    self.reps += 1
        else:
            if data: 
                self.currentState.updatePosition(data)

                if self.currentState.areConstraintsMet():
                    if self.nextState.isStateReached():
                        self.transitionToNextState()
                        if self.currentState.order == 0:
                            self.reps += 1
                            print ("rep done. reps: ",str(self.reps))
