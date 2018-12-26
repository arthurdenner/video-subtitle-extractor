import cv2
from datetime import timedelta
from pytesseract import image_to_string
from math import ceil, floor
def getTimeStamp(sec):
    timestamp = str(timedelta(seconds=sec))
    start = '{},000'.format(timestamp)
    end = '{},999'.format(timestamp)
    return '{} --> {}'.format(start, end)

def getSubtitleGroup(seq, timestamp,text):
    return '{}\n{}\n{}\n\n'.format(seq, timestamp, text)

def prepareSubtitle(videoFile):
    cap = cv2.VideoCapture(videoFile)
    frameRate = int(ceil(cap.get(cv2.CAP_PROP_FPS))) #frame rate
    totalFrames = int(ceil(cap.get(cv2.CAP_PROP_FRAME_COUNT))) #frame ratecap.get(cv2.CV_CAP_PROP_FRAME_COUNT)
    framesToGet = int(floor(totalFrames/frameRate))
    return ["" for i in range(framesToGet)]

def getText(frame, config=('-l eng --oem 1 --psm 3')):
    return image_to_string(frame, config=config)

def writeToFile(subtitles, path):
    with open(path, "w") as file: 
        file.writelines(subtitles)