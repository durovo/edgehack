from enum import Enum

class Direction(Enum):
    Concentric = -1
    Eccentric = 1
    Rest = 0

class BodyParts(Enum):
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