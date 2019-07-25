from readers import CameraReader, VideoReader
import os 
import torch
from models.with_mobilenet import PoseEstimationWithMobileNet
from modules.load_state import load_state
from Trainer import Trainer
from BicepCurl import BicepCurl
import threading


net = PoseEstimationWithMobileNet()
modelPath = os.path.join('checkpoints', 'checkpoint_iter_370000.pth')
checkpoint = torch.load(modelPath, map_location=processor)
load_state(net, checkpoint)
cpu = True

def get_frameProvider(vid=None):
    if vid is None:
        frame_provider = CameraReader(0,1)
    else:
        frame_provider = VideoReader(vid)
    
    return frame_provider

def start_bicepCurl(vid = None):
    frame_provider = get_frameProvider(vid)  
    bicepcurl = BicepCurl()
    trainer = Trainer(frame_provider,bicepcurl,net)
    trainer.start_training(cpu)

def stop_excercise():
    