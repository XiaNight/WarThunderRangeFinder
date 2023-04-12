import cv2
import numpy as np
import Util
import time
import os

def GlobalThresholdTest(image, center = 189, r = 2, threshold = cv2.THRESH_BINARY, title = "Figure"):
    processedScreenShots = []
    for i in range(-4, 5):
        _, temp = cv2.threshold(image, center + i * r, 255, threshold)
        processedScreenShots.append(temp)
    Util.ShowImages(*processedScreenShots, title=title)

def AdaptiveThresholdTest(image):
	_, result = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
	Util.ShowImages(result)

def HighlightScreenshot(screenshot, json, boxSize = 10, color = (0, 255, 0), width = 1):
    for enemy in json['E']:
        pos = enemy['P']
        top_left = (pos[0] - boxSize, pos[1] - boxSize)
        bottom_right = (pos[0] + boxSize, pos[1] + boxSize)
        cv2.rectangle(screenshot, top_left, bottom_right, (0, 255, 0), width)

    pos = json['S']
    top_left = (pos[0] - boxSize, pos[1] - boxSize)
    bottom_right = (pos[0] + boxSize, pos[1] + boxSize)
    cv2.rectangle(screenshot, top_left, bottom_right, color, width)

def TestScreenShot(testCase, selfArrow, squadPing, enemyMarks, mapRatio, DEBUG=False):
    # Load Image and trim screen shot
    screenshot = cv2.imread(testCase)
    screenshot = screenshot[990:1425, 2110:2545]

    start_time = time.time()
    success, json = Util.IdentifyScreenshot(screenshot, selfArrow, squadPing, enemyMarks, mapRatio=mapRatio, DEBUG=DEBUG)
    end_time = time.time()

    duration = end_time - start_time
    duration = round(duration * 1000, 2)
    print(testCase.split('\\')[-1], " took:", duration, " ms")

    if success:
        HighlightScreenshot(screenshot, json, width=2)

    return (success, json, screenshot, duration)

def GetPngFiles(folder_path):
    png_files = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.png'):
            png_files.append(os.path.join(folder_path, filename))
    return png_files

def MainTest(DEBUG=False):
    selfArrow, squadPing, enemyMarks = Util.LoadIcons()
    miniMapSize = 435
    mapSize = 1000
    mapRatio = mapSize / miniMapSize
    miniMapBbox = (2110, 990, 435, 435)

    # testCases = ['TestImage1.png', 'TestImage2.png', 'TestImage3.png', 'TestImage4.png']
    testCases = GetPngFiles("TestCases")
    print("Test Cases:", testCases)
    # testCases = ['TestImage1.png']

    resultImages = []
    resultDurations = []

    for testCase in testCases:
        try:
            (success, json, screenshot, duration) = TestScreenShot(testCase, selfArrow, squadPing, enemyMarks, mapRatio=mapRatio, DEBUG=True)
        except:
            print(testCase.split('\\')[-1], " causes and error.")
        resultImages.append(screenshot)
        resultDurations.append(duration)

    print("Totle Time: {0} ms".format(sum(resultDurations), 2))
    print("Average Time: {0} ms".format(round(sum(resultDurations) / len(resultDurations), 2)))

    # Show the result
    if DEBUG:
        Util.ShowImages(*resultImages)

if __name__ == "__main__":
    MainTest(True)