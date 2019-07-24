from Exercise import Exercise
from State import State
from Utils.Constants import Direction,BodyParts
from Utils.HelperMethods import displayText
from Constraint import Constraint
import numpy as np

class Squats(Exercise):
    def __init__(self):
        back_constraint = Constraint(self.isCorrectBack)
        lowerleg_constraint = Constraint(self.isLowerLegStraight)
        knee_constraint = Constraint(self.isCorrectKnee)
        self.constraints = [knee_constraint]
        statesList = self.getStates()
        super(Squats, self).__init__(statesList, "Squats")
        self.RESTANGLE_KNEE = 80
        self.RESTANGLE_BACK = 80
        self.RESTTHIGHANGLE = 80
        self.ACTIVETHIGHANGLE = 20
        self.CONCENTRICTHIGHANGLE = 70
        self.ECCENTRICTHIGHANGLE = 30

        self.MINBACKANGLE = 50
        self.MINKNEEANGLE = 50
    
    def setHuman(self, human):
        self.human = human
        self.side = BodyParts.LEFT.value if human.side.isStandingFacingLeft() else BodyParts.RIGHT.value
        self.lowerLegAngle = self.getLowerLegAngle()
        self.backAngle = self.getBackAngle()
        self.thighAngle = self.getThighAngle()

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

    def getThighAngle(self):
        return self.human.side.getSlopeAngle(BodyParts.HIP.value, BodyParts.KNEE.value, self.side)

    def isCorrectBack(self,raiseError=None):
        if raiseError:
            print ("Straighten your back: ", str(self.backAngle))
        return True if self.backAngle is np.nan else self.backAngle> self.MINBACKANGLE

    def isCorrectKnee(self,raiseError=None):
        if raiseError:
            print ("Knees too close.", str(self.backAngle))
        rightHip = self.human.front.getPoint(BodyParts.HIP.value, BodyParts.RIGHT.value)
        leftHip = self.human.front.getPoint(BodyParts.HIP.value, BodyParts.LEFT.value)
        rightKnee = self.human.front.getPoint(BodyParts.KNEE.value, BodyParts.RIGHT.value)
        leftKnee = self.human.front.getPoint(BodyParts.KNEE.value, BodyParts.LEFT.value)

        if not(rightHip.isNullPoint() or leftHip.isNullPoint() or rightKnee.isNullPoint() or leftKnee.isNullPoint()):
            return rightKnee.coord[0] <= rightHip.coord[0] and leftKnee.coord[0] >= leftHip.coord[0]
        else:
            return True

    def isLowerLegStraight(self, raiseError=None):
        if raiseError:
            print ("Align your knees to your feet: ", self.lowerLegAngle)

        return True if self.lowerLegAngle is np.nan else self.lowerLegAngle > self.MINKNEEANGLE

    def isInitialStateReached(self):
        #TOD): add other checks to see if he is standing
        if self.lowerLegAngle > self.RESTANGLE_KNEE and self.backAngle > self.RESTANGLE_BACK and self.thighAngle > self.RESTTHIGHANGLE:
            return True
        else:
            return False

    def getInitialState(self):
        state = State(self.constraints,0, self.isInitialStateReached, "Resting")

        return state
    
    def isConcentricStateReached(self): 
        if self.thighAngle <= self.CONCENTRICTHIGHANGLE:
            return True
        else:
            return False

    def isActiveStateReached(self):
        if self.thighAngle < self.ACTIVETHIGHANGLE:
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
        if self.thighAngle > self.ECCENTRICTHIGHANGLE:
            return True
        else:
            return False

    def getEccentricState(self):
        state = State(self.constraints,3, self.isEccentricStateReached, "Eccentric")
        return state
        
    def continueExercise(self):
        super().continueExercise(self.thighAngle)

    def displayText(self, frame,view):
        super().displayText(frame)
        if view == "side":
            displayText("Backangle: "+ str(self.backAngle),50,80,frame)
            displayText("Thigh angle"+ str(self.thighAngle),50,120,frame)
            displayText("lower leg angle"+ str(self.lowerLegAngle),50,150,frame)
