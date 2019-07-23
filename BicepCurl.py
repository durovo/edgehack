from Exercise import Exercise
from State import State
from Utils.Constants import Direction,BodyParts
from Constraint import Constraint
from Utils.HelperMethods import displayText

class BicepCurl(Exercise):
    def __init__(self):
        self.constraints = [Constraint(self.isCorrectElbow), Constraint(self.isCorrectBack)]
        statesList = self.getStates()
        super(BicepCurl, self).__init__(statesList, "bicepCurl")
        self.RESTANGLE = 150
        self.CONCENTRICANGLE = 140
        self.ACTIVEANGLE = 55
        self.ECCENTRICANGLE = 65

    def setHuman(self, human):
        self.human = human
        self.side = BodyParts.LEFT.value if human.isFacingLeft() else BodyParts.RIGHT.value
        self.elbowAngle = self.human.getJointAngle(BodyParts.HIP.value, BodyParts.SHOULDER.value, BodyParts.ELBOW.value, self.side)
        self.curlAngle = self.getCurlAngle()
        self.backAngle = self.getBackAngle()

    def getStates(self):
        restingState = self.getInitialState()
        concentricState = self.getConcentricState()        
        activeState = self.getActiveState()
        eccentricState = self.getEccentricState()

        return [restingState, concentricState, activeState, eccentricState]

    def getElbowAngle(self):
        return self.human.getJointAngle(BodyParts.HIP.value, BodyParts.SHOULDER.value, BodyParts.ELBOW.value, self.side)

    def getBackAngle(self):
        return self.human.getSlopeAngle(BodyParts.HIP.value, BodyParts.SHOULDER.value, self.side)

    def getCurlAngle(self):
        curlAngle = self.human.getJointAngle(BodyParts.SHOULDER.value, BodyParts.ELBOW.value, BodyParts.WRIST.value, self.side)
        print(curlAngle)
        return curlAngle

    def isCorrectElbow(self,raiseError=None):
        if raiseError:
            print ("Bring your elbow closer to your body. Elbow angle", str(self.elbowAngle))
        return self.elbowAngle < 40
    
    def isCorrectBack(self,raiseError=None):
        if raiseError:
            print ("Straighten your back. Back angle", str(self.backAngle))
        return self.backAngle > 80

    def isInitialStateReached(self):
        #TODO: add other checks to see if he is standing
        if self.curlAngle > self.RESTANGLE:
            return True
        else:
            return False

    def getInitialState(self):
        state = State(self.constraints,0, self.isInitialStateReached, "Resting")

        return state
    
    def isConcentricStateReached(self):
        if self.curlAngle < self.CONCENTRICANGLE:
            return True
        else:
            return False

    def isActiveStateReached(self):
        if self.curlAngle < self.ACTIVEANGLE:
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
        if self.curlAngle > self.ECCENTRICANGLE:
            return True
        else:
            return False

    def getEccentricState(self):
        state = State(self.constraints,3, self.isEccentricStateReached, "Eccentric")
        return state
        
    def continueExercise(self):
        super().continueExercise(self.curlAngle)

    def displayText(self, frame):
        super().displayText(frame)
        displayText("Curl angle: "+ str(round(self.curlAngle,2)),50,80,frame)
        displayText("Back angle: "+ str(round(self.backAngle,2)),50,100,frame)
