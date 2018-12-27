import cv2
from math import trunc, ceil, floor
import sys

BOTTOM = 'bottom'
TOP = 'top'


def getFrameRate(path):
    try:
        video = cv2.VideoCapture(path)
        return video.get(cv2.CAP_PROP_FPS)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise


def getFrameArea(frame):
    h, w = frame.shape
    return h*w


def cropFrame(frame, percent, position=BOTTOM):
    if(percent < 0 or percent > 1):
        raise ValueError('Porcentagem precisa ser valor entre 0 e 1')

    if(position != BOTTOM and position != TOP):
        raise ValueError('Posição precisa ser TOP ou BOTTOM')

    height, width, _ = frame.shape

    if(position == TOP):
        return frame[height:trunc(height*percent), 0:width]
    return frame[trunc(height*percent):height, 0:width]


def getWhiteRegion(frame):
    imageGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return cv2.inRange(imageGray, 200, 255)


def getSubtitleArea(frame):
    cropped = cropFrame(frame, 0.7)
    return getWhiteRegion(cropped)


def isBlack(frame, limiar=0.01):
    area = getFrameArea(frame)
    return cv2.countNonZero(frame) < area*limiar


def getTotalFrames(videoFile):
    cap = cv2.VideoCapture(videoFile)
    frameRate = int(ceil(cap.get(cv2.CAP_PROP_FPS)))
    totalFrames = int(ceil(cap.get(cv2.CAP_PROP_FRAME_COUNT)))
    return int(floor(totalFrames/frameRate))
