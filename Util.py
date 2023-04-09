import cv2
import numpy as np
import pyautogui
import pyttsx3 # speak
import math
import socket
import json

def TakeScreenShot(bbox=None):
    # Take a screenshot
    screenshot = pyautogui.screenshot(region=bbox)

    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    return screenshot

def FindIcon(screenshot, icon_template, debug=False):
    # Convert the screenshot and icon template to grayscale
    screenshot_gray = screenshot[:,:,2]
    icon_template_gray = icon_template[:,:,2]

    # Perform template matching
    result = cv2.matchTemplate(screenshot_gray, icon_template_gray, cv2.TM_CCOEFF_NORMED)

    # Find the location of the best match
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    top_left = max_loc

    # Check if the confidence is below the threshold
    if max_val < 0.8:
        return (screenshot, None)

    # Calculate the center
    h, w = icon_template_gray.shape
    center = (top_left[0] + w/2, top_left[1] + h/2)

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