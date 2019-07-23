from demo import infer_fast, extract_keypoints,group_keypoints
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
        bicepCurl = None
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

            trainee.updatePositions(pose_entries[0],all_keypoints)
            temp_frame = frame
            training_output.append(self.markTrainee(trainee, temp_frame))
            if self.excercise == "bicepCurl":
                if bicepCurl:
                    bicepCurl.setHuman(trainee)
                else:
                    bicepCurl = BicepCurl(trainee)
                bicepCurl.continueExercise()
        self.saveTrainingVideo(training_output)

    def saveTrainingVideo(self,framesList):
        height,width,layers=framesList[1].shape
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        video=cv2.VideoWriter('training_output.avi',fourcc,20.0,(width,height))

        for frame in framesList:
            video.write(frame)

        cv2.destroyAllWindows()
        video.release()

    def markTrainee(self,trainee,frame):
        for part in trainee.partIntMap.keys():
            partCoord = trainee.getCoordinate(part)
            if partCoord is not None:
                cv2.circle(frame,(int(partCoord[0]),int(partCoord[1])),3,(0,255,0),-1)

        return frame

    def check_state_forms(self):
        if self.excercise.state.is_motion_state:
                for form in self.excercise.state.forms:
                    is_form_correct = form.check()
                    if not is_form_correct:
                        self.mouth.speak(form.message)

    def check_state_direction(self):
        if self.excercise.state.is_motion_state:
            is_direction_correct = self.excercise.state.direction.check_direction()
            if not is_direction_correct:
                self.mouth.speak(self.excercise.state.direction.message)
