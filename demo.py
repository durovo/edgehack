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


def infer_fast(net, img1, img2, net_input_height_size, stride, upsample_ratio, cpu,
               pad_value=(0, 0, 0), img_mean=(128, 128, 128), img_scale=1/256):
    height, width, _ = img1.shape
    scale = net_input_height_size / height

    scaled_img1 = cv2.resize(img1, (0, 0), fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
    scaled_img2 = cv2.resize(img2, (0, 0), fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
    scaled_img1 = normalize(scaled_img1, img_mean, img_scale)
    scaled_img2 = normalize(scaled_img2, img_mean, img_scale)
    min_dims = [net_input_height_size, max(scaled_img1.shape[1], net_input_height_size)]
    padded_img1, pad = pad_width(scaled_img1, stride, pad_value, min_dims)
    padded_img2, pad2 = pad_width(scaled_img2, stride, pad_value, min_dims)

    tensor_img1 = torch.from_numpy(padded_img1).permute(2, 0, 1).float()
    tensor_img2 = torch.from_numpy(padded_img2).permute(2, 0, 1).float()    
    if not cpu:
        tensor_img = torch.stack((tensor_img1, tensor_img2))
        tensor_img = tensor_img.cuda()
        # tensor_img1 = tensor_img1.cuda()
        # tensor_img2 = tensor_img2.cuda()
    # tensor_img = torch.stack((tensor_img1, tensor_img2))
    stages_output = net(tensor_img)
    stage2_heatmaps = stages_output[-2]
    heatmaps = np.transpose(stage2_heatmaps[0].cpu().data.numpy(), (1, 2, 0))
    heatmaps = cv2.resize(heatmaps, (0, 0), fx=upsample_ratio, fy=upsample_ratio, interpolation=cv2.INTER_CUBIC)
    heatmaps2 = np.transpose(stage2_heatmaps[1].cpu().data.numpy(), (1, 2, 0))
    heatmaps2 = cv2.resize(heatmaps2, (0, 0), fx=upsample_ratio, fy=upsample_ratio, interpolation=cv2.INTER_CUBIC)

    stage2_pafs = stages_output[-1]
    pafs = np.transpose(stage2_pafs[0].cpu().data.numpy(), (1, 2, 0))
    pafs = cv2.resize(pafs, (0, 0), fx=upsample_ratio, fy=upsample_ratio, interpolation=cv2.INTER_CUBIC)
    pafs2 = np.transpose(stage2_pafs[1].cpu().data.numpy(), (1, 2, 0))
    pafs2 = cv2.resize(pafs2, (0, 0), fx=upsample_ratio, fy=upsample_ratio, interpolation=cv2.INTER_CUBIC)
    return heatmaps, pafs, scale, pad, heatmaps2, pafs2, scale, pad2

font                   = cv2.FONT_HERSHEY_SIMPLEX
bottomLeftCornerOfText = (10,500)
fontScale              = 1
fontColor              = (255,255,255)
lineType               = 2

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

def get_frameProvider(source,vid=None):
    if vid is None:
        frame_provider = CameraReader(0,1)
    else:
        frame_provider = VideoReader(vid)
    
    return frame_provider

def start_bicepCurl(source = None, vid = None):
    print(source, vid)
    frame_provider = get_frameProvider(source,vid)

    cpu = True if processor == "cpu" else False
    from Trainer import Trainer
    from BicepCurl import BicepCurl
    bicepcurl = BicepCurl()
    trainer = Trainer(frame_provider,bicepcurl,net)
    trainer.start_training(cpu)

def start_squats(source = None, vid = None):
    from Squats import Squats
    from Trainer import Trainer
    print(source, vid)
    cpu = True if processor == "cpu" else False
    frame_provider = get_frameProvider(source,vid)
    squats = Squats()
    trainer = Trainer(frame_provider,squats,net)
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
        start_bicepCurl(0)
    elif exercise == "pushup":
        vid = 'data/pushup/pushup.mp4'
        start_pushup(0, vid)
    elif exercise == "squats":
        #vid = 'data/squat/DhruvSquats.mp4'
        start_squats(0)
    else:
        print ("Please specifiy a valid exercise")
    
