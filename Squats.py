from Exercise import Exercise
from State import State
from Utils.Constants import Direction,BodyParts
from Constraint import Constraint

class Squats(Exercise):
    def __init__(self):
        self.constraints = [Constraint(self.isCorrectBack), Constraint(self.isLowerLegStraight)]
        statesList = self.getStates()
        super(BicepCurl, self).__init__(statesList, "Squats")
        self.RESTANGLE_KNEE = 170
        self.CONCENTRICANGLE_KNEE = 120
        self.ACTIVEANGLE_KNEE = 55
        self.ECCENTRICANGLE = 65

    def setHuman(self, human):
        self.human = human
        self.side = BodyParts.LEFT.value if human.isFacingLeft(human.pose_entries, human.all_keypoints) else BodyParts.RIGHT.value
        self.elbowAngle = self.human.getJointAngle(BodyParts.HIP.value, BodyParts.SHOULDER.value, BodyParts.ELBOW.value, self.side)
        self.kneeAngle = self.getKneeAngle()
        self.backAngle = self.getBackAngle()

    def getStates(self):
        restingState = self.getInitialState()
        concentricState = self.getConcentricState()        
        activeState = self.getActiveState()
        eccentricState = self.getEccentricState()

        return [restingState, concentricState, activeState, eccentricState]

    def getKneeAngle(self):
        return self.human.getJointAngle(BodyParts.HIP.value, BodyParts.KNEE.value, BodyParts.ANKLE.value, self.side)


    def getBackAngle(self):
        return self.human.getJointAngle(BodyParts.KNEE.value, BodyParts.HIP.value, BodyParts.SHOULDER.value, self.side)

    def getCurlAngle(self):
        curlAngle = self.human.getJointAngle(BodyParts.SHOULDER.value, BodyParts.ELBOW.value, BodyParts.WRIST.value, self.side)
        print(curlAngle)
        return curlAngle

    def isCorrectThigh(self,raiseError=None):
        if raiseError:
            print ("Keep your thighs parallel to the ground.", str(self.elbowAngle))
        kneeCoord = self.human.getCoordinate(BodyParts.KNEE + self.side)
        hipCoord = self.human.getCoordinate(BodyParts.HIP + self.side)
        return math.abs(kneeCoord[1]-hipCoord[1]) < 10
    
    def isCorrectBack(self,raiseError=None):
        if raiseError:
            print ("Straighten your back.", str(self.backAngle))
        return math.abs(self.backAngle - self.kneeAngle) > 20

    def isLowerLegStraight(self, raiseError=None):
        if raiseError:
            print ("Align your knees to your feet.")
        kneeCoord = self.human.getCoordinate(BodyParts.KNEE + self.side)
        ankleCoord = self.human.getCoordinate(BodyParts.ANKLE + self.side)
        return math.abs(kneeCoord[0]-ankleCoord[0]) < 10

    def isInitialStateReached(self):
        #TOD): add other checks to see if he is standing
        if self.kneeAngle > self.RESTANGLE:
            return True
        else:
            return False

    def getInitialState(self):
        state = State(Direction.Rest.value, self.constraints,0, self.isInitialStateReached, "Resting")

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
        state = State(Direction.Concentric.value, self.constraints,1, self.isConcentricStateReached, "Concentric")
        return state

    def getActiveState(self):
        state = State(Direction.Rest.value, self.constraints,2, self.isActiveStateReached, "Active")
        return state
    
    def isEccentricStateReached(self):
        if self.curlAngle > self.ECCENTRICANGLE:
            return True
        else:
            return False

    def getEccentricState(self):
        state = State(Direction.Eccentric.value, self.constraints,3, self.isEccentricStateReached, "Eccentric")
        return state
        
    def continueExercise(self):
        super().continueExercise(self.curlAngle)
