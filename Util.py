import cv2
import numpy as np
import pyautogui
import pyttsx3 # speak
import math
import socket
import json
import matplotlib.pyplot as plt

def TakeScreenShot(bbox=None):
    # Take a screenshot
    screenshot = pyautogui.screenshot(region=bbox)

    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    return screenshot

def FindIcon(screenshot, icon_template, confidence=0.8, debug=False):
    # Convert the screenshot and icon template to grayscale
    screenshot_gray = screenshot[:,:,2]
    icon_template_gray = icon_template[:,:,2]

    # Perform template matching
    result = cv2.matchTemplate(screenshot_gray, icon_template_gray, cv2.TM_CCOEFF_NORMED)

    # Find the location of the best match
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    top_left = max_loc

    # Check if the confidence is below the threshold
    if max_val < confidence:
        return (screenshot, None)

    # Calculate the center
    h, w = icon_template_gray.shape
    center = (int(top_left[0] + w/2), int(top_left[1] + h/2))

    # Draw a rectangle around the matched icon
    bottom_right = (top_left[0] + w, top_left[1] + h)
    if debug:
        cv2.rectangle(screenshot, top_left, bottom_right, (0, 255, 0), 1)

    return (screenshot, center)

def FindIcons(screenshot, icon_template, confidence_threshold=0.8, debug=False, debug_color = (0, 255, 0)):
    # Convert the screenshot and icon template to grayscale
    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    icon_template_gray = cv2.cvtColor(icon_template, cv2.COLOR_BGR2GRAY)

    # Perform template matching
    result = cv2.matchTemplate(screenshot_gray, icon_template_gray, cv2.TM_CCOEFF_NORMED)

    # Find the locations of all matches above the confidence threshold
    locations = np.where(result >= confidence_threshold)
    matches = list(zip(*locations[::-1]))

    # Matched Centers
    centers = []

    # Draw a rectangle around each matched icon
    h, w = icon_template_gray.shape
    for top_left in matches:
        bottom_right = (top_left[0] + w, top_left[1] + h)
        centers.append((top_left[0] + w/2, top_left[1] + h/2))
        if debug:
            cv2.rectangle(screenshot, top_left, bottom_right, debug_color, -1)

    return screenshot, centers

def Speak(text):
    # Initialize the text-to-speech engine
    engine = pyttsx3.init()

    # Set the speech rate and volume
    engine.setProperty('rate', 150)  # Speed in words per minute
    engine.setProperty('volume', 1.0)  # Volume, from 0.0 to 1.0

    # Speak the text
    engine.say(text)
    engine.runAndWait()

def CalculateDistance(pos1, pos2):
    # Calculate the distance between the two poses
    dx = pos2[0] - pos1[0]
    dy = pos2[1] - pos1[1]
    distance = math.sqrt(dx**2 + dy**2)
    return distance

def ToJson(dictionary):
	return json.dumps(dictionary)

def ShowImg(image):
    imS = cv2.resize(image, (1080, 1080))
    cv2.imshow('Screenshot with matched icon', imS)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def ShowImages(*images, title="Figure"):
    n_images = len(images)
    n_rows = int(np.sqrt(n_images))
    n_cols = int(np.ceil(n_images / n_rows))

    fig, ax = plt.subplots(n_rows, n_cols, figsize=(10, 10))
    fig.suptitle(title)

    for i, image in enumerate(images):
        row = i // n_cols
        col = i % n_cols
        ax[row, col].imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        ax[row, col].axis('off')

    plt.show()

def LoadIcons():
    # Load the icon template
    squadPing = cv2.imread('SquadPing.png')
    selfArrow = cv2.imread('SelfArrow.png')

    LT = cv2.imread('LT.png')
    MT = cv2.imread('MT.png')
    HT = cv2.imread('HT.png')
    TD = cv2.imread('TD.png')
    SPAA = cv2.imread('SPAA.png')
    return selfArrow, squadPing, [LT, MT, HT, TD, SPAA]

def IdentifyScreenshot(screenshot, selfIcon, squadPingIcon, enemyMarks, mapRatio, DEBUG=False):
    # Highlight Icons
    # _, screenshot = cv2.threshold(screenshot, 189, 255, cv2.THRESH_TOZERO)

    # Process the yellow mask for self and squad mark
    # yellow_mask = cv2.bitwise_and(screenshot[:,:,2], screenshot[:,:,1])

    # Calculate Enemy Distances
    markers = []
    json = {}

    # Find the icon in the screenshot
    (screenshot, selfArrowCenter) = FindIcon(screenshot, selfIcon, 0.7, DEBUG)
    (screenshot, squadPingCenter) = FindIcon(screenshot, squadPingIcon, 0.7, DEBUG)

    # If failed to find self, abort
    if selfArrowCenter == None:
        return False, None

    json['S'] = selfArrowCenter
    json['R'] = mapRatio
    convertedDistance = None

    # If squad ping is found
    if squadPingCenter != None:
        distance = CalculateDistance(selfArrowCenter, squadPingCenter)
        convertedDistance = int(distance * mapRatio)
        markers.append({"P": squadPingCenter, "D": convertedDistance})
        json['Sq'] = squadPingCenter
        json['D'] = convertedDistance
    else:
        json['Sq'] = (0, 0)
        json['D'] = 0


    # Find Enemies Icons
    threashHold = 0.7
    for enemyMark in enemyMarks:
        (_, marks) = FindIcons(screenshot, enemyMark, threashHold, DEBUG, (0, 0, 255))
        for mark in marks:
            d = int(CalculateDistance(selfArrowCenter, mark) * mapRatio)
            markers.append({"P": mark, "D": d})
        
    print(markers)
    json["E"] = markers
    return True, json