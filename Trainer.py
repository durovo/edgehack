from human import *
from demo import infer_fast, extract_keypoints,group_keypoints
from BicepCurl import BicepCurl
import cv2
from Utils.HelperMethods import displayText
from GlobalHelpers import global_state

class Trainer(object):
    def __init__(self, frame_provider, excercise, net):
        self.frame_provider = frame_provider
        self.excercise = excercise
        self.net = net

    def start_training(self,cpu):
        trainee = Human()
        training_output=[]
        cnt = 0
        for side_frame,front_frame in self.frame_provider:
            if not global_state.continue_training:
                global_state.rep_count = self.excercise.reps
                break
            net = self.net.eval()
            if not cpu:
                net = self.net.cuda()

            stride = 8
            upsample_ratio = 4
            height_size = 256
            total_keypoints_num = 0
            total_keypoints_num2 = 0

            heatmaps, pafs, scale, pad, heatmaps2, pafs2, scale2, pad2 = infer_fast(net, side_frame, front_frame, height_size, stride, upsample_ratio, cpu)
            all_keypoints_by_type = []
            all_keypoints_by_type2 = []
            for kpt_idx in range(18):  # 19th for bg
                total_keypoints_num += extract_keypoints(heatmaps[:, :, kpt_idx], all_keypoints_by_type, total_keypoints_num)
                total_keypoints_num2 += extract_keypoints(heatmaps2[:, :, kpt_idx], all_keypoints_by_type2, total_keypoints_num2)

            pose_entries, all_keypoints = group_keypoints(all_keypoints_by_type, pafs, demo=True)
            pose_entries2, all_keypoints2 = group_keypoints(all_keypoints_by_type2, pafs2, demo=True)
            for kpt_id in range(all_keypoints.shape[0]):
                all_keypoints[kpt_id, 0] = (all_keypoints[kpt_id, 0] * stride / upsample_ratio - pad[1]) / scale
                all_keypoints[kpt_id, 1] = (all_keypoints[kpt_id, 1] * stride / upsample_ratio - pad[0]) / scale
            for kpt_id in range(all_keypoints2.shape[0]):
                all_keypoints2[kpt_id, 0] = (all_keypoints2[kpt_id, 0] * stride / upsample_ratio - pad2[1]) / scale2
                all_keypoints2[kpt_id, 1] = (all_keypoints2[kpt_id, 1] * stride / upsample_ratio - pad2[0]) / scale2
            if len(pose_entries) * len(pose_entries2) != 0:
                
                trainee.side.updatePositions(pose_entries[0],all_keypoints)
                trainee.front.updatePositions(pose_entries2[0], all_keypoints2)
                
                self.excercise.setHuman(trainee)
                self.excercise.continueExercise()

                if self.excercise.currentState and self.excercise.currentState.isToleranceExceeded():
                    self.excercise.reset()
                
                self.markTrainee(trainee.side, side_frame,self.excercise)
                self.markTrainee(trainee.front, front_frame,self.excercise)

            if not cpu:
                output_frame = np.concatenate((side_frame,front_frame), axis=1)
                training_output.append(output_frame)
                print("showing image")
                cv2.imshow('Output',output_frame)

                key = cv2.waitKey(33)
                if key == 27:
                    break
        
        # self.saveTrainingVideo(training_output)
        global_state.stopped = True

    def saveTrainingVideo(self,framesList):
        height,width,layers=framesList[0].shape
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        video=cv2.VideoWriter('test_training_output.avi',fourcc,10,(width,height))

        for frame in framesList:
            video.write(frame)

        cv2.destroyAllWindows()
        video.release()

    def markTrainee(self,trainee,frame,exercise):
        for part in trainee.partIntMap.keys():
            partCoord = trainee.getCoordinate(part)
            if partCoord is not None:
                cv2.circle(frame,(int(partCoord[0]),int(partCoord[1])),3,(0,255,0),-1)
        # kneeCoord = trainee.side.getCoordinate(LEFT + KNEE)
        # hipCoord = trainee.side.getCoordinate(LEFT+HIP)
        # if exercise.currentState is not None:
        #         # displayText("Distance: " + str(exercise.distanceFromGround),50,20,frame)
        #         # displayText("Error: " + str(exercise.continuousConstraintViolations),50,30,frame)
        #         displayText("Reps: "+ str(exercise.reps),50,40,frame)
        #         displayText(exercise.currentState.name,50,60,frame)
        # if kneeCoord is not None:
        #     wkaAngle = trainee.side.getJointAngle(HIP, KNEE, ANKLE, LEFT)
        #     displayText(str(wkaAngle), kneeCoord[0], kneeCoord[1], frame)

        #     hipAngle = trainee.side.getJointAngle(SHOULDER, HIP, KNEE, LEFT)
        #     displayText(str(hipAngle), hipCoord[0], hipCoord[1], frame)
        # # curlCoord = trainee.getCoordinate(exercise.side+4)
        # # if curlCoord is not None:
        # #     displayText(str(exercise.curlAngle),curlCoord[0],curlCoord[1],frame)
        # #     displayText("Reps: "+ str(exercise.reps),50,50,frame)
        # #     displayText(exercise.currentState.name,50,100,frame)

        exercise.displayText(frame,trainee.view)

        return frame

    def check_state_forms(self):
        if self.excercise.state.is_motion_state:
                for form in self.excercise.state.forms:
                    is_form_correct = form.check()
                    if not is_form_correct:
                        self.mouth.speak(form.message)
        
        exercise.displayText(frame)

        return frame