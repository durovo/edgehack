from PostureUtil import Point
import numpy as np

LEFT = 100
RIGHT = 200
HIP = 1
KNEE = 2
NOSE = 3
ELBOW = 4
SHOULDER = 5
CHEST = 6
EYE = 7
WRIST = 8
ANKLE = 9
EAR = 10

class Human(object):
    def __init__(self):
        self.side = Skeleton("side")
        self.front = Skeleton("front")
    

class Skeleton(object):
    def __init__(self, view):
        self.view = view
        self.initPartsDict()
    
    def updatePositions(self, keypoints_dict):
        self.keypoints_dict = keypoints_dict

    def getJointAngle(self, joint1, fulcrum, joint2, side=0):
        joint1Point = self.getPoint(joint1,side)
        joint2Point = self.getPoint(joint2,side)
        fulcrumPoint = self.getPoint(fulcrum,side)
        return fulcrumPoint.getJointAngle(joint1Point, joint2Point)

    def getSlopeAngle(self, joint1, joint2, side = 0):
        joint1Point = self.getPoint(joint1,side)
        joint2Point = self.getPoint(joint2,side)

        return joint1Point.getSlopeAngle(joint2Point)     

    def getBodyPartDistance(self,part1,part2, side=0):
        part1Point = self.getPoint(part1, side)
        part2Point =  self.getPoint(part2, side)

        return part1Point.distance(part2Point)
        
    def getCoordinate(self, joint):
        #print(joint)
        
        keyPointKey = self.keypoints_dict['keypoints'][0][self.partIntMap[joint]][2].data.cpu().numpy()
        # print(keyPointKey)
        if keyPointKey >= 0:
            return self.keypoints_dict['keypoints'][0][self.partIntMap[joint]][0:2].data.cpu().numpy()
        else:
            return None

    def getPoint(self, joint, side=0):
        joint = joint+side
        return Point(self.getCoordinate(joint))

    def initPartsDict(self):
        self.partIntMap = {
            101: 11,
            201: 12,
            102: 13,
            202: 14,
            3: 0,
            104: 7,
            204: 8,
            205: 6,
            105: 5,
            6: 1,
            107: 1,
            207: 2,
            208: 10,
            108: 9,
            209: 16,
            109: 15,
            110: 3,
            210: 4
        }

    def isFacingLeft(self):
        side = LEFT
        part1 = HIP
        part2 = SHOULDER
        part3 = ELBOW

        p1_c = self.getCoordinate(side+part1)
        p2_c = self.getCoordinate(side+part2)
        p3_c = self.getCoordinate(side+part3)

        if p2_c[0] < p1_c[0]:
            return True
        return False

    def isStandingFacingLeft(self):
        side = LEFT
        part1 = EAR
        part2 = EYE
        part1_global = self.getCoordinate(side+part1)
        if part1_global is None:
            side = RIGHT
        part1 = self.getCoordinate(side+part1)
        part2 = self.getCoordinate(side+part2)

        if part2[0] < part1[0]:
            return True
        return False

    def isBodyHorizontal(self,side):
        hip = self.getPoint(HIP, side)
        shoulder = self.getPoint(SHOULDER, side)

        if(shoulder.isNullPoint() or hip.isNullPoint()):
            return False
        
        horizontal_disp = abs(shoulder.coord[0] - hip.coord[0])

        if horizontal_disp > 30:
            return True
        else:
            return False
    
