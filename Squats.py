from Exercise import Exercise
from State import State
from Utils.Constants import Direction,BodyParts
from Constraint import Constraint

class Squats(Exercise):
    def __init__(self):
        back_constraint = Constraint(self.isCorrectBack)
        lowerleg_constraint = Constraint(self.isLowerLegStraight)
        thigh_constraint = Constraint(self.isCorrectThigh)
        self.rest_constraints = [back_constraint, lowerleg_constraint]
        self.motion_constraints = self.rest_constraints
        self.active_constraints = [back_constraint, lowerleg_constraint, thigh_constraint]
        statesList = self.getStates()
        super(Squats, self).__init__(statesList, "Squats")
        self.RESTANGLE_KNEE = 170
        self.RESTANGLE_HIP = 170
        self.CONCENTRICANGLE_KNEE = 120
        self.ACTIVEANGLE_KNEE = 100
        self.ECCENTRICANGLE = 65

    def setHuman(self, human):
        self.human = human
        self.side = BodyParts.LEFT.value if human.isFacingLeft(human.pose_entries, human.all_keypoints) else BodyParts.RIGHT.value
        self.kneeAngle = self.getKneeAngle()
        self.backAngle = self.getBackAngle()
        self.hipAngle = self.getHipAngle()

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

    def getHipAngle(self):
        return self.human.getJointAngle(BodyParts.SHOULDER.value, BodyParts.HIP.value, BodyParts.KNEE.value, self.side)

    def isCorrectThigh(self,raiseError=None):
        if raiseError:
            print ("Keep your thighs parallel to the ground.")
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
        if self.kneeAngle > self.RESTANGLE_KNEE and self.hipAngle > self.RESTANGLE_HIP:
            return True
        else:
            return False

    def getInitialState(self):
        state = State(Direction.Rest.value, self.rest_constraints,0, self.isInitialStateReached, "Resting")

        return state
    
    def isConcentricStateReached(self):
        if self.kneeAngle < self.RESTANGLE_KNEE:
            return True
        else:
            return False

    def isActiveStateReached(self):
        if self.kneeAngle < self.ACTIVEANGLE_KNEE:
            return True
        else:
            return False

    def getConcentricState(self):
        state = State(Direction.Concentric.value, self.motion_constraints,1, self.isConcentricStateReached, "Concentric")
        return state

    def getActiveState(self):
        state = State(Direction.Rest.value, self.active_constraints,2, self.isActiveStateReached, "Active")
        return state
    
    def isEccentricStateReached(self):
        if self.kneeAngle > self.ACTIVEANGLE_KNEE:
            return True
        else:
            return False

    def getEccentricState(self):
        state = State(Direction.Eccentric.value, self.motion_constraints,3, self.isEccentricStateReached, "Eccentric")
        return state
        
    def continueExercise(self):
        super().continueExercise(self.kneeAngle)
