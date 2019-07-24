import cv2
import numpy as np

class ImageReader(object):
    def __init__(self, file_names):
        self.file_names = file_names
        self.max_idx = len(file_names)

    def __iter__(self):
        self.idx = 0
        return self

    def __next__(self):
        if self.idx == self.max_idx:
            raise StopIteration
        img = cv2.imread(self.file_names[self.idx], cv2.IMREAD_COLOR)
        if img.size == 0:
            raise IOError('Image {} cannot be read'.format(self.file_names[self.idx]))
        self.idx = self.idx + 1
        return img

class CameraReader(object):
    def __init__(self, source1,source2=None):
        self.source1 = source1
        self.source2 = source2
        self.cap1 = cv2.VideoCapture(self.source1)
        self.cap2 = cv2.VideoCapture(self.source2)
        self.isOpened1 = True
        self.isOpened2 = True
        if not self.cap1.isOpened():
            self.isOpened1 = False
        if not self.cap2.isOpened():
            self.isOpened2 = False

    def __iter__(self):
        if not self.cap1.isOpened() and not self.cap2.isOpened():
            raise IOError('Video {} cannot be opened'.format("webcam"))
        return self

    def __next__(self):
        was_read1, img1 = self.cap1.read()
        was_read2, img2 = self.cap2.read()

        if not was_read1:
            raise StopIteration
        if not was_read2:
            img2 = np.zeros_like(img1)
        return img1,img2

class VideoReader(object):
    def __init__(self, file_name):
        self.file_name = file_name
        try:  # OpenCV needs int to read from webcam
            self.file_name = int(file_name)
        except ValueError:
            pass

    def __iter__(self):
        self.cap = cv2.VideoCapture(self.file_name)
        # self.cap = cv2.VideoCapture(1)
        if not self.cap.isOpened():
            raise IOError('Video {} cannot be opened'.format(self.file_name))
        return self

    def __next__(self):
        was_read, img = self.cap.read()
        if not was_read:
            raise StopIteration
        return img

