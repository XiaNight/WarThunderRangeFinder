import cv2
import numpy as np
import Util

def GlobalThresholdTest(image, center = 189, r = 2, threshold = cv2.THRESH_BINARY, title = "Figure"):
    processedScreenShots = []
    for i in range(-4, 5):
        _, temp = cv2.threshold(image, center + i * r, 255, threshold)
        processedScreenShots.append(temp)
    Util.ShowImages(*processedScreenShots, title=title)

def AdaptiveThresholdTest(image):
	_, result = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
	Util.ShowImages(result)

def MainTest():
	