from PostureUtil import Point

class Human(object):
    def __init__(self):
        self.initPartsDict();
    
    def updatePositions(self, pose_entries, all_keypoints):
        self.pose_entries = pose_entries
        self.all_keypoints = all_keypoints

    def getJoinAngle(self, joint1, fulcrum, joint2):
        joint1Point = self.getPoint(joint1)
        joint2Point = self.getPoint(joint2)
        fulcrumPoint = self.getPoint(fulcrumPoint)
        return fulcrumPoint.getAngle(joint1Point, joint2Point)

    def getPoint(self, joint):
        coordinate = self.all_keypoints[self.pose_entries[partIntMap[joint]], 0:2]
        return new Point(coordinate)

    def initPartsDict(self):
        self.partIntMap = {
            'leftHip': 11,
            'rightHip': 8,
            'leftKnee': 12,
            'rightKnee': 9,
            'nose': 0,
            'leftElbow': 6,
            'rightElbow': 3,
            'rightShoulder': 2,
            'leftShoulder': 5,
            'chestCenter': 1,
            'leftEye': 15,
            'rightEye': 14,
            'rightWrist': 4,
            'leftWrist': 7,
            'rightAnkle': 10,
            'leftAnkle': 13,
            'leftEar': 16,
            'rightEar': 17
        }
        self.LEFT = 100
        self.RIGHT = 200
        self.HIP = 1
        self.KNEE = 2
        self.NOSE = 3
        self.ELBOW = 4
        self.SHOULDER = 5
        self.CENTER = 6
        self.EYE = 7
        self.WRIST = 8
        self.ANKLE = 9
        self.EAR = 10

    