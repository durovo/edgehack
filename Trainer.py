from demo import infer_fast, extract_keypoints,group_keypoints
from human import Human
from BicepCurl import BicepCurl

class Trainer(object):
    def __init__(self, frame_provider, excercise, net):
        self.frame_provider = frame_provider
        self.excercise = excercise
        self.net = net

    def start_training(self):
        human = Human()
        for frame in self.frame_provider:
            net = self.net.eval()

            stride = 8
            upsample_ratio = 4
            height_size = 256
            cpu = True
            total_keypoints_num = 0

            heatmaps, pafs, scale, pad = infer_fast(net, frame, height_size, stride, upsample_ratio, cpu)
            all_keypoints_by_type = []
            for kpt_idx in range(18):  # 19th for bg
                total_keypoints_num += extract_keypoints(heatmaps[:, :, kpt_idx], all_keypoints_by_type, total_keypoints_num)
            pose_entries, all_keypoints = group_keypoints(all_keypoints_by_type, pafs, demo=True)
            for kpt_id in range(all_keypoints.shape[0]):
                all_keypoints[kpt_id, 0] = (all_keypoints[kpt_id, 0] * stride / upsample_ratio - pad[1]) / scale
                all_keypoints[kpt_id, 1] = (all_keypoints[kpt_id, 1] * stride / upsample_ratio - pad[0]) / scale

            human.updatePositions(pose_entries[0],all_keypoints)

            if self.excercise == "bicepCurl":
                bicepCurl = BicepCurl(human)
                bicepCurl.continueExercise()

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
