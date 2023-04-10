import cv2
import numpy as np
import Util
import time

def GlobalThresholdTest(image, center = 189, r = 2, threshold = cv2.THRESH_BINARY, title = "Figure"):
    processedScreenShots = []
    for i in range(-4, 5):
        _, temp = cv2.threshold(image, center + i * r, 255, threshold)
        processedScreenShots.append(temp)
    Util.ShowImages(*processedScreenShots, title=title)

def AdaptiveThresholdTest(image):
	_, result = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
	Util.ShowImages(result)

def MainTest(DEBUG=False):
    selfArrow, squadPing, enemyMarks = Util.LoadIcons()
    miniMapSize = 435
    mapSize = 1000
    mapRatio = mapSize / miniMapSize
    miniMapBbox = (2110, 990, 435, 435)

    screenshot = cv2.imread('TestImage3.png')
    screenshot = screenshot[990:1325, 2110:2545]


    start_time = time.time()
    success, json = Util.IdentifyScreenshot(screenshot, selfArrow, squadPing, enemyMarks, mapRatio=mapRatio, DEBUG=DEBUG)
    end_time = time.time()

    duration = end_time - start_time
    print("Identification duration:", duration)

    if success == False:
        # Util.Speak("失敗")
        return

    if json['D'] != 0:
    	pass
        # Util.Speak(int(json['D']))
    else:
    	pass
        # Util.Speak("無標示點")

    # Show the result
    if DEBUG:
    	Util.ShowImg(screenshot)

if __name__ == "__main__":
    start_time = time.time()
    MainTest()
    end_time = time.time()
    duration = end_time - start_time
    print("Total duration:", duration)