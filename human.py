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
        self.side = Skeleton()
        self.front = Skeleton()
    

class Skeleton(object):
    def __init__(self):
        self.initPartsDict()
    
    def updatePositions(self, pose_entries, all_keypoints):
        self.pose_entries = pose_entries
        self.all_keypoints = all_keypoints

    def getJointAngle(self, joint1, fulcrum, joint2, side=0):
        joint1Point = self.getPoint(joint1,side)
        joint2Point = self.getPoint(joint2,side)
        fulcrumPoint = self.getPoint(fulcrum,side)
        return fulcrumPoint.getJointAngle(joint1Point, joint2Point)

    def getCoordinate(self, joint):
        #print(joint)
        keyPointKey = int(self.pose_entries[self.partIntMap[joint]])
        if keyPointKey >= 0:
            return self.all_keypoints[keyPointKey, 0:2]
        else:
            return None

    def getPoint(self, joint, side=0):
        joint = joint+side
        return Point(self.getCoordinate(joint))

    def initPartsDict(self):
        self.partIntMap = {
            101: 11,
            201: 8,
            102: 12,
            202: 9,
            3: 0,
            104: 6,
            204: 3,
            205: 2,
            105: 5,
            6: 1,
            107: 15,
            207: 14,
            208: 4,
            108: 7,
            209: 10,
            109: 13,
            110: 16,
            210: 17
        }

    def isFacingLeft(self, pose_entries, all_keypoints):
        side = LEFT
        part1 = HIP
        part2 = SHOULDER
        part3 = ELBOW
        part1_global = self.pose_entries[self.partIntMap[side+part1]]
        if part1_global == -1:
            side = RIGHT
            part1_global = self.pose_entries[self.partIntMap[side+part1]]
        part1 = all_keypoints[int(part1_global), 0:2]
        part2_global = self.pose_entries[self.partIntMap[side+part2]]
        part2 = all_keypoints[int(part2_global), 0:2]
        part3_global = self.pose_entries[self.partIntMap[side+part3]]
        part3 = all_keypoints[int(part3_global), 0:2]

        td = part2-part3
        if part2[0] < part1[0]:
            return True
        return False