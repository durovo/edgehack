import numpy as np

'''
Usage:
from PostureUtils import Point
pose_entry = pose_entries[0]
#Making the point objects
p1 = Point(pose_entry, all_keypoints, "left", "Shoulder")
p2 = Point(pose_entry, all_keypoints, "chestCenter")
p3 = Point(pose_entry, all_keypoints,"nose")
#Get angle formed at p2 by the lines joining p2 with p1 and p3
print("angle : " + str(p2.getJointAngle(p1,p3)))
'''
class Point:
    def __init__(self, coordinates):
        self.coord = coordinates
    
    def distance(self, otherPoint):
        if self.isNullPoint() or otherPoint.isNullPoint():
            return np.nan
        return np.square((self.coord[0]-otherPoint.coord[0])) + np.square((self.coord[1]-otherPoint.coord[1]))
    
    def isNullPoint(self):
        return self.coord is None

    def getJointAngle(self,point1,point2):
        if self.isNullPoint() or point1.isNullPoint() or point2.isNullPoint():
            return np.nan
            
        line1 = point1.coord - self.coord
        line2 = point2.coord - self.coord

        cosine_angle = np.dot(line1, line2) / (np.linalg.norm(line1) * np.linalg.norm(line2))
        angle = np.arccos(cosine_angle)

        return np.degrees(angle)
    
    def getSlopeAngle(self,otherPoint):
        if self.isNullPoint() or otherPoint.isNullPoint():
            return np.nan

        slope = np.arctan(abs((otherPoint.coord[1] - self.coord[1])/(otherPoint.coord[0] - self.coord[0])))

        return np.degrees(slope)  