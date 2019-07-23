from demo import infer_fast, extract_keypoints,group_keypoints,displayText
from human import Human
from BicepCurl import BicepCurl
import cv2

class Trainer(object):
    def __init__(self, frame_provider, excercise, net):
        self.frame_provider = frame_provider
        self.excercise = excercise
        self.net = net

    def start_training(self,cpu):
        trainee = Human()
        training_output=[]
        cnt = 0
        for frame in self.frame_provider:
            net = self.net.eval()
            if not cpu:
                net = self.net.cuda()

            stride = 8
            upsample_ratio = 4
            height_size = 256
            total_keypoints_num = 0

            heatmaps, pafs, scale, pad = infer_fast(net, frame, height_size, stride, upsample_ratio, cpu)
            all_keypoints_by_type = []
            for kpt_idx in range(18):  # 19th for bg
                total_keypoints_num += extract_keypoints(heatmaps[:, :, kpt_idx], all_keypoints_by_type, total_keypoints_num)
            pose_entries, all_keypoints = group_keypoints(all_keypoints_by_type, pafs, demo=True)
            for kpt_id in range(all_keypoints.shape[0]):
                all_keypoints[kpt_id, 0] = (all_keypoints[kpt_id, 0] * stride / upsample_ratio - pad[1]) / scale
                all_keypoints[kpt_id, 1] = (all_keypoints[kpt_id, 1] * stride / upsample_ratio - pad[0]) / scale

            if len(pose_entries) == 0:
                continue
                
            trainee.updatePositions(pose_entries[0],all_keypoints)
            self.excercise.setHuman(trainee)
            self.excercise.continueExercise()

            if self.excercise.continuousConstraintViolations > 10:
                self.excercise.reset()
            
            training_output.append(self.markTrainee(trainee, frame,self.excercise))
            #cv2.imwrite('testImg.png',frame)
            if not cpu:
                cv2.imshow('Output',frame)
                key = cv2.waitKey(33)
                if key == 27:
                    return
        
        self.saveTrainingVideo(training_output)

    def saveTrainingVideo(self,framesList):
        height,width,layers=framesList[1].shape
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        video=cv2.VideoWriter('training_output.avi',fourcc,20.0,(width,height))

        for frame in framesList:
            video.write(frame)

        cv2.destroyAllWindows()
        video.release()

    def markTrainee(self,trainee,frame,exercise):
        for part in trainee.partIntMap.keys():
            partCoord = trainee.getCoordinate(part)
            if partCoord is not None:
                cv2.circle(frame,(int(partCoord[0]),int(partCoord[1])),3,(0,255,0),-1)
        
        if exercise.currentState is not None:
            displayText("Distance: " + str(exercise.distanceFromGround),50,20,frame)
            displayText("Error: " + str(exercise.continuousConstraintViolations),50,30,frame)
            displayText("Reps: "+ str(exercise.reps),50,40,frame)
            displayText(exercise.currentState.name,50,60,frame)

        return frame