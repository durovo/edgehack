from Exercise import Exercise
from State import State
from Utils.Constants import Direction,BodyParts
from Utils.HelperMethods import displayText
from Constraint import Constraint
import numpy as np

class Squats(Exercise):
    def __init__(self,tts):
        self.tts = tts
        self.resetViolations()
        back_constraint = Constraint(self.isCorrectBack, self.backToleranceExceeded)
        lowerleg_constraint = Constraint(self.isLowerLegStraight, self.lowerLegToleranceExceeded)
        knee_constraint = Constraint(self.isCorrectKnee, self.kneeToleranceExceeded)
        self.constraints = [knee_constraint]
        statesList = self.getStates()
        super(Squats, self).__init__(statesList, "Squats")
        self.RESTANGLE_KNEE = 80
        self.RESTANGLE_BACK = 80
        self.RESTTHIGHANGLE = 80
        self.MAXFRONTTHIGHANGLE = 85
        self.ACTIVETHIGHANGLE = 20
        self.CONCENTRICTHIGHANGLE = 70
        self.ECCENTRICTHIGHANGLE = 30

        self.MAXBACKVIOLATIONS = 5
        self.MAXLOWERLEGVIOLATIONS = 5
        self.MAXKNEEVIOLATIONS = 1

        self.MINBACKANGLE = 50
        self.MINKNEEANGLE = 50

    def resetViolations(self):
        self.backViolations = 0
        self.lowerLegViolations = 0
        self.kneeViolations = 0
    
    def setHuman(self, human):
        self.human = human
        self.side = BodyParts.LEFT.value if human.side.isStandingFacingLeft() else BodyParts.RIGHT.value
        self.lowerLegAngle = self.getLowerLegAngle()
        self.backAngle = self.getBackAngle()
        self.leftThighAngle = self.getThighAngle("front", BodyParts.LEFT.value)
        self.rightThighAngle = self.getThighAngle("front", BodyParts.RIGHT.value)
        self.squatAngle = self.getThighAngle("side", self.side)

    def getStates(self):
        restingState = self.getInitialState()
        concentricState = self.getConcentricState()        
        activeState = self.getActiveState()
        eccentricState = self.getEccentricState()

        return [restingState, concentricState, activeState, eccentricState]

    def getLowerLegAngle(self):
        return self.human.side.getSlopeAngle(BodyParts.KNEE.value, BodyParts.ANKLE.value, self.side)

    def getBackAngle(self):
        return self.human.side.getSlopeAngle(BodyParts.HIP.value, BodyParts.SHOULDER.value, self.side)

    def getThighAngle(self, view, side):
        human = self.human.side if view == "side" else self.human.front
        return human.getSlopeAngle(BodyParts.HIP.value, BodyParts.KNEE.value, side)

    def backToleranceExceeded(self):
        return self.backViolations >= self.MAXBACKVIOLATIONS

    def lowerLegToleranceExceeded(self):
        return self.lowerLegViolations >= self.MAXLOWERLEGVIOLATIONS

    def kneeToleranceExceeded(self):
        return self.kneeViolations >= self.MAXKNEEVIOLATIONS

    def isCorrectBack(self,raiseError=None):
        if raiseError and not self.backAngle is np.nan:
            self.tts.BotSpeak(3, "Straighten back")            
            print ("Straighten your back: ", str(self.backAngle))
            self.backViolations += 1
        return True if self.backAngle is np.nan else self.backAngle> self.MINBACKANGLE

    def isCorrectKnee(self,raiseError=None):
        if raiseError and not self.backAngle is np.nan:
            self.tts.BotSpeak(4, "Widen knees")            
            print ("Knees too close.", str(self.backAngle))
            self.kneeViolations += 1
        
        return self.leftThighAngle < self.MAXFRONTTHIGHANGLE and self.rightThighAngle < self.MAXFRONTTHIGHANGLE

    def isLowerLegStraight(self, raiseError=None):
        if raiseError and not self.lowerLegAngle is np.nan:
            self.tts.BotSpeak(5, "Move knees back")            
            print ("Align your knees to your feet: ", self.lowerLegAngle)
            self.lowerLegViolations += 1

        return True if self.lowerLegAngle is np.nan else self.lowerLegAngle > self.MINKNEEANGLE

    def isInitialStateReached(self):
        #TOD): add other checks to see if he is standing
        if self.lowerLegAngle > self.RESTANGLE_KNEE and self.backAngle > self.RESTANGLE_BACK and self.squatAngle > self.RESTTHIGHANGLE:
            return True
        else:
            return False

    def getInitialState(self):
        state = State(self.constraints,0, self.isInitialStateReached, "Resting")

        return state
    
    def isConcentricStateReached(self): 
        if self.squatAngle <= self.CONCENTRICTHIGHANGLE:
            return True
        else:
            return False

    def isActiveStateReached(self):
        if self.squatAngle < self.ACTIVETHIGHANGLE:
            return True
        else:
            return False

    def getConcentricState(self):
        state = State(self.constraints,1, self.isConcentricStateReached, "Concentric")
        return state

    def getActiveState(self):
        state = State(self.constraints,2, self.isActiveStateReached, "Active")
        return state
    
    def isEccentricStateReached(self):
        if self.squatAngle > self.ECCENTRICTHIGHANGLE:
            return True
        else:
            return False

    def getEccentricState(self):
        state = State(self.constraints,3, self.isEccentricStateReached, "Eccentric")
        return state
        
    def continueExercise(self):
        super().continueExercise(self.squatAngle)

    def displayText(self, frame,view):
        super().displayText(frame)
        if view == "side":
            displayText("Backangle: "+ str(self.backAngle),50,80,frame)
            displayText("Thigh angle"+ str(self.squatAngle),50,120,frame)
            displayText("lower leg angle"+ str(self.lowerLegAngle),50,150,frame)
            displayText("Left thigh angle" + str(self.leftThighAngle), 50,180, frame)
            displayText("Right thigh angle" + str(self.rightThighAngle), 50,210, frame)
