from Exercise import Exercise
from State import State
from Utils.Constants import Direction,BodyParts
from Constraint import Constraint
import numpy as np

class Pushup(Exercise):
    def __init__(self):
        self.constraints = [Constraint(self.isCorrectBack)]
        statesList = self.getStates()
        super(Pushup, self).__init__(statesList, "pushup")
        self.RESTHANDANGLE = 160
        self.RESTBACKANGLE = 160
        self.CONCENTRICANGLE = 140
        self.ACTIVEHANDANGLE = 55
        self.ECCENTRICHANDANGLE = 65

    def setHuman(self, human):
        self.human = human
        self.side = BodyParts.LEFT.value if human.isFacingLeft() else BodyParts.RIGHT.value
        self.elbowAngle = self.human.getJointAngle(BodyParts.HIP.value, BodyParts.SHOULDER.value, BodyParts.ELBOW.value, self.side)
        self.handAngle = self.getHandAngle()
        self.backAngle = self.getBackAngle()
        self.elbowDistanceFromHead = self.getElbowDistanceFromHead()

    def getStates(self):
        restingState = self.getInitialState()
        concentricState = self.getConcentricState()        
        activeState = self.getActiveState()
        eccentricState = self.getEccentricState()

        return [restingState, concentricState, activeState, eccentricState]

    def getHandAngle(self):
        handAngle = self.human.getJointAngle(BodyParts.SHOULDER.value, BodyParts.ELBOW.value, BodyParts.WRIST.value, self.side)
        return handAngle

    def getBackAngle(self):
        backAngle = self.human.getJointAngle(BodyParts.KNEE.value, BodyParts.HIP.value, BodyParts.SHOULDER.value, self.side)
        return backAngle

    def getElbowDistanceFromHead(self):
        elbowDistanceFromHead = self.human.getBodyPartDistance(BodyParts.ELBOW.value, BodyParts.EAR.value, self.side)
        print("elbowDistanceFromHead", str(elbowDistanceFromHead))

        return elbowDistanceFromHead
    
    def isCorrectElbow(self,raiseError=None):
        if raiseError:
            if self.elbowDistanceFromHead is not np.nan:
                print ("Bring your elbow closer to your body. Elbow angle", str(self.elbowDistanceFromHead))
        return self.elbowDistanceFromHead < 40
    
    def isCorrectBack(self,raiseError=None):
        if raiseError:
            print ("Straighten your back. Back angle", str(self.backAngle))
        return self.backAngle > 160

    def isInitialStateReached(self):
        #TOD): add other checks to see if he is standing
        if (self.human.isBodyHorizontal(self.side) and self.handAngle > self.RESTHANDANGLE and self.backAngle > self.RESTBACKANGLE):
            return True
        else:
            return False
        
    def getInitialState(self):
        state = State(Direction.Rest.value, self.constraints,0, self.isInitialStateReached, "Resting")

        return state
    
    def isConcentricStateReached(self):
        if self.handAngle < self.CONCENTRICANGLE:
            return True
        else:
            return False

    def isActiveStateReached(self):
        if self.handAngle < self.ACTIVEHANDANGLE:
            return True
        else:
            return False

    def getConcentricState(self):
        state = State(Direction.Concentric.value, self.constraints,1, self.isConcentricStateReached, "Concentric")
        return state

    def getActiveState(self):
        state = State(Direction.Rest.value, self.constraints,2, self.isActiveStateReached, "Active")
        return state
    
    def isEccentricStateReached(self):
        if self.handAngle > self.ECCENTRICHANDANGLE:
            return True
        else:
            return False

    def getEccentricState(self):
        state = State(Direction.Eccentric.value, self.constraints,3, self.isEccentricStateReached, "Eccentric")
        return state
    
    def continueExercise(self):
        wristCoord = self.human.getPoint(BodyParts.WRIST.value, self.side)
        shoulderCoord = self.human.getPoint(BodyParts.SHOULDER.value, self.side)
        if wristCoord.isNullPoint() or shoulderCoord.isNullPoint():
            self.distanceFromGround = np.nan
        else:
            self.distanceFromGround = abs(wristCoord.coord[1] - shoulderCoord.coord[1])
        
        super().continueExercise(self.distanceFromGround)