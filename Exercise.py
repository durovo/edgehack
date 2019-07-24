import numpy as np
from Utils.HelperMethods import displayText

class Exercise:
    def __init__(self, statesList, name = None):
        self.stateFlow = statesList
        self.currentState = None
        self.nextState = statesList[0]
        self.name = name
        self.reps  = -1
        self.isExerciseReset = False

    def setHuman(self,human):
        pass

    def calculateNextState(self):
        return self.stateFlow[(self.currentState.order + 1) % len(self.stateFlow)]

    def transitionToNextState(self):
        self.currentState = self.nextState
        self.nextState = self.calculateNextState()

    def checkAndUpdateState(self):
        if self.nextState.isStateReached():
            self.transitionToNextState()
            print ("State order: ",str(self.currentState.order))
            if self.currentState.order == 0:
                if self.isExerciseReset:
                    self.isExerciseReset = False
                else:
                    self.reps += 1
                
                print ("rep done. reps: ",str(self.reps))

    def reset(self):
        print ("Reseting rep")
        self.nextState = self.stateFlow[0]
        self.isExerciseReset = True
        self.resetViolations()
    
    def continueExercise(self, data):
        if self.currentState is None:
            self.checkAndUpdateState()
        elif data is not np.nan:
            self.currentState.updatePosition(data)
            
            if self.currentState.areConstraintsMet():
                self.checkAndUpdateState()
            else:
                self.currentState.constraintViolations += 1

    def displayText(self, frame):
        if self.currentState is not None:
            displayText("Reps: "+ str(self.reps),50,40,frame)
            displayText(self.currentState.name,50,60,frame)

    def resetViolations():
        pass