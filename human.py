from PostureUtil import Point


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
        self.initPartsDict();
    
    def updatePositions(self, pose_entries, all_keypoints):
        self.pose_entries = pose_entries
        self.all_keypoints = all_keypoints

    def getJoinAngle(self, joint1, fulcrum, joint2):
        joint1Point = self.getPoint(joint1)
        joint2Point = self.getPoint(joint2)
        fulcrumPoint = self.getPoint(fulcrum)
        return fulcrumPoint.getJointAngle(joint1Point, joint2Point)
    def getCoordinate(self, joint):
        print(joint)
        return self.all_keypoints[int(self.pose_entries[self.partIntMap[joint]]), 0:2]
    def getPoint(self, joint):
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

    