import argparse
import cv2
import numpy as np
import torch
import math
import time
import os 

from models.with_mobilenet import PoseEstimationWithMobileNet
from modules.keypoints import extract_keypoints, group_keypoints, BODY_PARTS_KPT_IDS, BODY_PARTS_PAF_IDS
from modules.load_state import load_state
from val import normalize, pad_width
from human import *
from Checker import Checker
from readers import ImageReader, CameraReader, VideoReader


def infer_fast(net, img, net_input_height_size, stride, upsample_ratio, cpu,
               pad_value=(0, 0, 0), img_mean=(128, 128, 128), img_scale=1/256):
    height, width, _ = img.shape
    scale = net_input_height_size / height

    scaled_img = cv2.resize(img, (0, 0), fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
    scaled_img = normalize(scaled_img, img_mean, img_scale)
    min_dims = [net_input_height_size, max(scaled_img.shape[1], net_input_height_size)]
    padded_img, pad = pad_width(scaled_img, stride, pad_value, min_dims)

    tensor_img = torch.from_numpy(padded_img).permute(2, 0, 1).unsqueeze(0).float()
    if not cpu:
        tensor_img = tensor_img.cuda()

    stages_output = net(tensor_img)

    stage2_heatmaps = stages_output[-2]
    heatmaps = np.transpose(stage2_heatmaps.squeeze().cpu().data.numpy(), (1, 2, 0))
    heatmaps = cv2.resize(heatmaps, (0, 0), fx=upsample_ratio, fy=upsample_ratio, interpolation=cv2.INTER_CUBIC)

    stage2_pafs = stages_output[-1]
    pafs = np.transpose(stage2_pafs.squeeze().cpu().data.numpy(), (1, 2, 0))
    pafs = cv2.resize(pafs, (0, 0), fx=upsample_ratio, fy=upsample_ratio, interpolation=cv2.INTER_CUBIC)

    return heatmaps, pafs, scale, pad

font                   = cv2.FONT_HERSHEY_SIMPLEX
bottomLeftCornerOfText = (10,500)
fontScale              = 1
fontColor              = (255,255,255)
lineType               = 2

def run_demo(net, image_provider, height_size, cpu):
    net = net.eval()
    if not cpu:
        net = net.cuda()

    stride = 8
    upsample_ratio = 4
    color = [0, 224, 255]

    current_human = Human()
    for img in image_provider:
        orig_img = img.copy()
        heatmaps, pafs, scale, pad = infer_fast(net, img, height_size, stride, upsample_ratio, cpu)

        total_keypoints_num = 0
        all_keypoints_by_type = []
        for kpt_idx in range(18):  # 19th for bg
            total_keypoints_num += extract_keypoints(heatmaps[:, :, kpt_idx], all_keypoints_by_type, total_keypoints_num)

        pose_entries, all_keypoints = group_keypoints(all_keypoints_by_type, pafs, demo=True)
        for kpt_id in range(all_keypoints.shape[0]):
            all_keypoints[kpt_id, 0] = (all_keypoints[kpt_id, 0] * stride / upsample_ratio - pad[1]) / scale
            all_keypoints[kpt_id, 1] = (all_keypoints[kpt_id, 1] * stride / upsample_ratio - pad[0]) / scale
        # print(len(pose_entries))
        # print("parts__")
        
        kpLocations = dict()
        
        # print("Pose entries: ", len(pose_entries))
        for n in range(len(pose_entries)):
            # if len(pose_entries[n]) <10:
            #     continue
            # if not checkDistance(pose_entries[n], all_keypoints, "left", "Shoulder", "Ankle"):
            #     continue
            # if not checkDistance(pose_entries[n], all_keypoints, "left", "Elbow", "Hip"):
            #     continue
            # if not checkDistance(pose_entries[n], all_keypoints, "left", "Shoulder", "Hip"):
            #     continue
            # if not checkDistance(pose_entries[n], all_keypoints, "left", "Shoulder", "Knee"):
            #     continue
            # if not checkDistance(pose_entries[n], all_keypoints, "left", "Shoulder", "Ankle"):
            #     continue
            # if not checkDistance(pose_entries[n], all_keypoints, "left", "Elbow", "Hip"):
            #     continue
            # if not checkDistance(pose_entries[n], all_keypoints, "left", "Elbow", "Knee"):
            #     continue
            current_human.updatePositions(pose_entries[n], all_keypoints)
            angle = current_human.getJointAngle(LEFT+ HIP, 
                                                LEFT+ KNEE,
                                                LEFT+ ANKLE)
            point = current_human.getCoordinate(LEFT+KNEE)
            printAngle(angle, point[0], point[1], img)
            for part_id in range(len(BODY_PARTS_PAF_IDS) - 2):
                kpt_a_id = BODY_PARTS_KPT_IDS[part_id][0]
                global_kpt_a_id = pose_entries[n][kpt_a_id]
                if global_kpt_a_id != -1:
                    x_a, y_a = all_keypoints[int(global_kpt_a_id), 0:2]

                    cv2.circle(img, (int(x_a), int(y_a)), 3, color, -1)
                    # cv2.putText(img, str(kpt_a_id), 
                    #             (int(x_a), int(y_a)), 
                    #             font, 
                    #             fontScale,
                    #             fontColor,
                    #             lineType)
                kpt_b_id = BODY_PARTS_KPT_IDS[part_id][1]
                global_kpt_b_id = pose_entries[n][kpt_b_id]
                if global_kpt_b_id != -1:
                    x_b, y_b = all_keypoints[int(global_kpt_b_id), 0:2]
                    cv2.circle(img, (int(x_b), int(y_b)), 3, color, -1)
                if global_kpt_a_id != -1 and global_kpt_b_id != -1:
                    cv2.line(img, (int(x_a), int(y_a)), (int(x_b), int(y_b)), color, 2)
                # print(part_id, (x_a, y_a), (x_b, y_b))

        img = cv2.addWeighted(orig_img, 0.6, img, 0.4, 0)
        cv2.imshow('Lightweight Human Pose Estimation Python Demo', img)
        # cv2.imwrite("output.jpeg", img)
        key = cv2.waitKey(33)
        if key == 27:  # esc
            return

def isFacingLeft(pose_entries, all_keypoints):
    side = "left"
    part1 = "Hip"
    part2 = "Shoulder"
    part3 = "Elbow"
    part1_global = pose_entries[partIntMap[side+part1]]
    if part1_global == -1:
        side = "right"
        part1_global = pose_entries[partIntMap[side+part1]]
    part1 = all_keypoints[int(part1_global), 0:2]
    part2_global = pose_entries[partIntMap[side+part2]]
    part2 = all_keypoints[int(part2_global), 0:2]
    part3_global = pose_entries[partIntMap[side+part3]]
    part3 = all_keypoints[int(part3_global), 0:2]

    td = part2-part3
    esDistance = np.sqrt(np.inner(td, td))
    if part2[0] < part1[0]:
        return True
    return False

def printAngle(angle, x, y, img, font_color=(255, 255, 255)):
    if not math.isnan(angle):
        angle = int(angle)
    displayText(angle, x, y, img, font_color)

def checkDistance(pose_entries, all_keypoints, side, part1, part2):
    part1_global = pose_entries[partIntMap[side+part1]]
    part1 = all_keypoints[int(part1_global), 0:2]
    part2_global = pose_entries[partIntMap[side+part2]]
    part2 = all_keypoints[int(part2_global), 0:2]
    distance = np.square((part1[0]-part2[0])) + np.square((part1[1]-part2[1]))
    if distance < 20:
        return False
    return True
partIntMap = {
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
class Struct:
    def __init__(self, **entries): self.__dict__.update(entries)

def drawLinesTriplets(pose_entries, all_keypoints, img, color, side, part1L, part2L, part3L):
    part1_global = pose_entries[partIntMap[side+part1L]]
    part1 = all_keypoints[int(part1_global), 0:2]
    cv2.circle(img, (int(part1[0]), int(part1[1])), 3, color, -1)
    font                   = cv2.FONT_HERSHEY_SIMPLEX
    bottomLeftCornerOfText = (10,500)
    fontScale              = 1
    fontColor              = (255,255,255)
    lineType               = 2
    cv2.putText(img, part1L, 
                    (int(part1[0]), int(part1[1])), 
                    font, 
                    fontScale,
                    fontColor,
                    lineType)
    part2_global = pose_entries[partIntMap[side+part2L]]
    part2 = all_keypoints[int(part2_global), 0:2]
    cv2.circle(img, (int(part2[0]), int(part2[1])), 3, color, -1)
    cv2.putText(img, part2L, 
                    (int(part2[0]), int(part2[1])), 
                    font, 
                    fontScale,
                    fontColor,
                    lineType)
    part3_global = pose_entries[partIntMap[side+part3L]]
    part3 = all_keypoints[int(part3_global), 0:2]
    cv2.circle(img, (int(part3[0]), int(part3[1])), 3, color, -1)
    cv2.putText(img, part3L, 
                    (int(part3[0]), int(part3[1])), 
                    font, 
                    fontScale,
                    fontColor,
                    lineType)
    cv2.line(img, (int(part1[0]), int(part1[1])), (int(part2[0]), int(part2[1])), color, 2)
    cv2.line(img, (int(part2[0]), int(part2[1])), (int(part3[0]), int(part3[1])), color, 2)



import sys
if len(sys.argv) > 1:
    processor = sys.argv[1]
    exercise = sys.argv[2] if len(sys.argv) > 2 else None
else:
    processor = "cpu"
    exercise = None

net = PoseEstimationWithMobileNet()
modelPath = os.path.join('checkpoints', 'checkpoint_iter_370000.pth')
checkpoint = torch.load(modelPath, map_location=processor)
load_state(net, checkpoint)


def start_planks(source=0,vid=None):
    # accuracy_queue.put("from demo fun")
    frame_provider = CameraReader(source)
    if vid is not None:
        frame_provider = VideoReader(vid)
    height_size = 256
    cpu = True if processor == "cpu" else False
    run_demo(net, frame_provider, height_size, cpu)

def get_frameProvider(source,vid):
    if vid is not None:
        frame_provider = CameraReader(0)
        if not frame_provider.isOpened:
            frame_provider = VideoReader(vid)
    elif source is not None:
        vid = []
        for filename in os.listdir(source):
            vid.append(os.path.join(source, filename))
        frame_provider = ImageReader(vid)
    
    return frame_provider

def start_bicepCurl(source = None, vid = None):
    print(source, vid)
    frame_provider = get_frameProvider(source,vid)

    cpu = True if processor == "cpu" else False
    from Trainer import Trainer
    from BicepCurl import BicepCurl
    bicepCurl = BicepCurl()
    trainer = Trainer(frame_provider,bicepCurl,net)
    trainer.start_training(cpu)

def start_pushup(source = None, vid = None):
    print(source, vid)
    frame_provider = get_frameProvider(source,vid)

    cpu = True if processor == "cpu" else False
    from Trainer import Trainer
    from Pushup import Pushup
    pushup = Pushup()
    trainer = Trainer(frame_provider,pushup,net)
    trainer.start_training(cpu)

if __name__ == '__main__':
    if exercise == "bicepcurl":
        vid = 'data/bcurl/bicepCurl.mp4'
        # start_planks(0, vid)
        start_bicepCurl(0,vid)
    elif exercise == "pushup":
        vid = 'data/pushup/pushup.mp4'
        start_pushup(0, vid)
    else:
        print ("Please specifiy a valid exercise")
    
