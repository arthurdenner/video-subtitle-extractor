import cv2
import math
import pytesseract
from PIL import Image
import frame
import subtitle
import os

videoFile = "video.mp4"
imagesFolder = './frames/{}/'.format(videoFile)
subtitles = subtitle.prepareSubtitle(videoFile)
cap = cv2.VideoCapture(videoFile)
frameRate = frame.getFrameRate(videoFile)
count = 1

if not os.path.exists(imagesFolder):
    os.makedirs(imagesFolder)

cap.set(cv2.CAP_PROP_POS_AVI_RATIO, 1)
totalSeconds = cap.get(cv2.CAP_PROP_POS_MSEC)/1000 - 1
cap.set(cv2.CAP_PROP_POS_AVI_RATIO, 0)

while(cap.isOpened()):
    frameId = cap.get(1)  # current frame number
    ret, fr, = cap.read()

    if (ret != True):
        break

    sec = math.floor(cap.get(cv2.CAP_PROP_POS_MSEC)/1000)
    secLeft = int(math.ceil(totalSeconds)) - sec
    message = 'Analysing second {}. {} seconds left'.format(sec, secLeft)
    print(message, end='\r')
    if (frameId % math.floor(frameRate) == 0):
        subtitleArea = frame.getSubtitleArea(fr)
        if (not frame.isBlack(subtitleArea)):
            filename = imagesFolder + "/second_" + str(count) + ".jpg"
            cv2.imwrite(filename, subtitleArea)
            text = subtitle.getText(subtitleArea)
            timestamp = subtitle.getTimeStamp(sec)
            subtitles[sec] = subtitle.getSubtitleGroup(count, timestamp, text)
            count += 1

cap.release()
subtitle.writeToFile(subtitles, "video.srt")
