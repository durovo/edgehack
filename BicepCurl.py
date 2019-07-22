from Exercise import Exercise
from State import State
from Utils.Constants import Direction,BodyParts
from Constraint import Constraint

class BicepCurl(Exercise):
    def __init__(self, human):
        self.human = human
        self.side = BodyParts.LEFT.value if human.isFacingLeft(human.pose_entries, human.all_keypoints) else BodyParts.RIGHT.value
        self.constraints = [Constraint(self.isCorrectElbow), Constraint(self.isCorrectBack)]
        self.elbowAngle = self.human.getJointAngle(BodyParts.HIP.value, BodyParts.SHOULDER.value, BodyParts.ELBOW.value, self.side)
        statesList = self.getStates()
        super(BicepCurl, self).__init__(statesList, "bicepCurl")

    def getStates(self):
        restingState = self.getInitialState()
        concentricState = self.getConcentricState()        
        activeState = self.getActiveState()
        eccentricState = self.getEccentricState()

        return [restingState, concentricState, activeState, eccentricState]

    def getElbowAngle(self):
        return self.human.getJointAngle(BodyParts.HIP.value, BodyParts.SHOULDER.value, BodyParts.ELBOW.value, self.side)


    def getBackAngle(self):
        return self.human.getJointAngle(BodyParts.HIP.value, BodyParts.SHOULDER.value, BodyParts.ELBOW.value, self.side)

    def getCurlAngle(self):
        return self.human.getJointAngle(BodyParts.SHOULDER.value, BodyParts.ELBOW.value, BodyParts.WRIST.value, self.side)

    def isCorrectElbow(self):
        return self.getElbowAngle() < 40
    
    def isCorrectBack(self):
        return self.getBackAngle() > 160

    def isInitialStateReached(self):
        #TOD): add other checks to see if he is standing
        if self.getCurlAngle() > 160:
            return True
        else:
            return False

    def getInitialState(self):
        state = State(Direction.Rest.value, self.constraints,0, self.isInitialStateReached)

        return state
    
    def isConcentricStateReached(self):
        if self.getCurlAngle() < 160:
            return True
        else:
            return False

    def isActiveStateReached(self):
        if self.getCurlAngle() < 30:
            return True
        else:
            return False

    def getConcentricState(self):
        state = State(Direction.Concentric.value, self.constraints,1, self.isConcentricStateReached)
        return state

    def getActiveState(self):
        state = State(Direction.Rest.value, self.constraints,2, self.isActiveStateReached)
        return state
    
    def isEccentricStateReached(self):
        if self.getCurlAngle() > 30:
            return True
        else:
            return False

    def getEccentricState(self):
        state = State(Direction.Eccentric.value, self.constraints,3, self.isEccentricStateReached)
        return state
        
    def continueExercise(self):
        super().continueExercise(self.getCurlAngle())
