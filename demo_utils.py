from readers import CameraReader, VideoReader
import os 
import torch
from models.with_mobilenet import PoseEstimationWithMobileNet
from modules.load_state import load_state
from Trainer import Trainer
from BicepCurl import BicepCurl
from Pushup import Pushup
from Squats import Squats
import TextToSpeech as tts

cpu = False
processor = "cuda"
if cpu: processor = "cpu"
net = PoseEstimationWithMobileNet()
modelPath = os.path.join('checkpoints', 'checkpoint_iter_370000.pth')
checkpoint = torch.load(modelPath, map_location=processor)
load_state(net, checkpoint)


def get_frameProvider(vid=None):
    if vid is None:
        frame_provider = CameraReader(0,1)
    else:
        frame_provider = VideoReader(vid)
    
    return frame_provider

def start_bicepcurl(vid = None):
    frame_provider = get_frameProvider()  
    bicepcurl = BicepCurl(tts)
    trainer = Trainer(frame_provider,bicepcurl,net)
    trainer.start_training(cpu)

def start_pushups(vid = None):
    frame_provider = get_frameProvider()  
    pushup = Pushup(tts)
    trainer = Trainer(frame_provider,pushup,net)
    trainer.start_training(cpu)

def start_squats(vid = None):
    frame_provider = get_frameProvider()  
    squats = Squats(tts)
    trainer = Trainer(frame_provider,squats,net)
    trainer.start_training(cpu)